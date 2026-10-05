#!/usr/bin/env python3
"""Independent browser scenarios and deterministic network controls.

Only outcome/equality/structural metrics are persisted. Request bodies, credentials,
tokens and exports remain in memory. Exact-SHA release required for product mode.
"""
import argparse
import asyncio
import copy
import json
from pathlib import Path
import re
import secrets
import time
from urllib.parse import urlsplit, parse_qs

from playwright.async_api import async_playwright, expect
import stage1_campaign as prior
import oracle
from campaign import API

check = prior.check


class Traffic:
    def __init__(self, origin):
        self.origin = origin.rstrip('/')
        self.api_target = self.origin
        self.assets_target = self.origin
        self.legacy_single_bridge = False
        self.bookings = []
        self.blocked_hosts = set()
        self.delayed = None
        self.loss = None
        self.api_paths = ('/auth/', '/restaurants', '/availability', '/reservations', '/reservation-moves', '/_test/')

    async def handler(self, route):
        req = route.request
        parsed = urlsplit(req.url)
        if parsed.scheme in ('data', 'blob', 'about'):
            await route.continue_(); return
        if parsed.netloc != urlsplit(self.origin).netloc:
            self.blocked_hosts.add(parsed.hostname or 'unknown')
            await route.abort('blockedbyclient'); return
        is_api = parsed.path.startswith(self.api_paths)
        payload = req.post_data
        if parsed.path == '/reservations' and req.method == 'POST':
            original = json.loads(payload)
            effective = copy.deepcopy(original)
            if self.legacy_single_bridge and 'table_ids' in effective and len(effective['table_ids']) == 1:
                effective['table_id'] = effective.pop('table_ids')[0]
                payload = prior.encode_json(effective)
            headers = await req.all_headers()
            self.bookings.append({'body': original, 'effective_body': effective,
                                  'key': headers.get('idempotency-key'), 'authorization': headers.get('authorization')})
        if self.loss and parsed.path == '/reservations' and req.method == 'POST':
            kind = self.loss; self.loss = None
            if kind == 'after':
                response = await route.fetch(url=self.api_target + parsed.path, post_data=payload, timeout=5000)
                self.last_committed = await response.json()
                check(response.status == 201, 'lost-response setup did not commit')
            await route.abort('failed'); return
        gate = self.delayed
        if gate and gate['match'](req) and not gate['started'].is_set():
            response = await route.fetch(url=(self.api_target + parsed.path + ('?' + parsed.query if parsed.query else '')) if is_api else req.url,
                                         post_data=payload, timeout=5000)
            gate['started'].set()
            await gate['release'].wait()
            try:
                await route.fulfill(response=response)
            except Exception:
                # A product cancelling an obsolete request also satisfies late-response isolation.
                if not req.failure:
                    raise
            finally:
                gate['finished'].set()
            return
        if not is_api and self.assets_target != self.origin:
            response = await route.fetch(url=self.assets_target + parsed.path + ('?' + parsed.query if parsed.query else ''), timeout=5000)
            await route.fulfill(response=response)
        elif is_api and (self.api_target != self.origin or payload != req.post_data):
            response = await route.fetch(url=self.api_target + parsed.path + ('?' + parsed.query if parsed.query else ''),
                                         post_data=payload, timeout=10000 if parsed.path.startswith('/_test/') else 5000)
            if self.legacy_single_bridge and parsed.path == '/availability' and response.status == 200:
                value = await response.json()
                if any('available_options' not in slot for slot in value['slots']):
                    rid = parse_qs(parsed.query)['restaurant_id'][0]
                    details = await route.fetch(url=self.api_target + '/restaurants/' + rid, method='GET', post_data=None, timeout=5000)
                    restaurant = await details.json()
                    capacities = {t['id']: t['capacity'] for t in restaurant['tables']}
                    for slot in value['slots']:
                        slot.setdefault('available_options', [{'table_ids': [tid], 'capacity': capacities[tid]}
                                                              for tid in slot['available_table_ids']])
                    await route.fulfill(response=response, json=value)
                else:
                    await route.fulfill(response=response)
            else:
                await route.fulfill(response=response)
        else:
            await route.continue_()

    def gate(self, match):
        self.delayed = {'match': match, 'started': asyncio.Event(), 'release': asyncio.Event(), 'finished': asyncio.Event()}
        return self.delayed


class BrowserCampaign:
    def __init__(self, browser, origin, destination, legacy, diagnostics, control=None):
        self.browser = browser
        self.origin = origin.rstrip('/')
        self.api = API(self.origin)
        self.destination = API(destination or origin)
        self.legacy = prior.API(legacy) if legacy else None
        self.out = Path(diagnostics)
        self.control = Path(control) if control else None
        self.results = []
        self.visual_metrics = []
        self.traffics = []

    async def call(self, fn, *args, **kwargs):
        return await asyncio.to_thread(fn, *args, **kwargs)

    async def fresh(self, width=1280, fx=None):
        fx = fx or oracle.fixture()
        await self.call(self.api.reset, fx)
        context = await self.browser.new_context(viewport={'width': width, 'height': 900}, timezone_id='Asia/Tokyo')
        context.set_default_timeout(10000)
        traffic = Traffic(self.origin)
        self.traffics.append(traffic)
        await context.route('**/*', traffic.handler)
        page = await context.new_page()
        await page.goto(self.origin + '/', wait_until='domcontentloaded')
        return context, page, traffic, fx

    async def login(self, page, user='ada'):
        await page.goto(self.origin + '/login', wait_until='domcontentloaded')
        await page.get_by_test_id('login-email').fill(user + '@verifier.invalid')
        await page.get_by_test_id('login-password').fill(prior.PASSWORD)
        await page.get_by_test_id('login-submit').click()
        await expect(page.get_by_test_id('current-user')).to_contain_text(user)
        check(await page.get_by_test_id('auth-error').count() == 0, 'auth-error remains after login')
        await page.goto(self.origin + '/', wait_until='domcontentloaded')

    async def search(self, page, party=2, day=prior.DAY, restaurant='r'):
        await page.get_by_test_id('restaurant-select').select_option(restaurant)
        await page.get_by_test_id('date-input').fill(day)
        await page.get_by_test_id('party-size-input').fill(str(party))
        await page.get_by_test_id('search-button').click()

    async def select(self, page, ids=('a', 'z'), at='18:00'):
        cell = page.get_by_test_id('slot-' + '+'.join(ids) + '-' + at)
        await expect(cell).to_have_attribute('data-available', 'true')
        await cell.click()
        await expect(page.get_by_test_id('booking-form')).to_be_visible()

    async def grid(self, page, fx, party, day=prior.DAY, restaurant='r', occupied=()):
        expected = oracle.slots(fx, day, party, occupied, restaurant)
        if not expected:
            await expect(page.get_by_test_id('no-slots')).to_be_visible()
            check(await page.get_by_test_id('availability-grid').count() == 0, 'empty day still has grid')
            return
        await expect(page.get_by_test_id('availability-grid')).to_be_visible()
        r = next(x for x in fx['restaurants'] if x['id'] == restaurant)
        for slot in expected:
            local = slot['starts_at_local'][-5:]
            for table in r['tables']:
                cell = page.get_by_test_id('slot-' + table['id'] + '-' + local)
                await expect(cell).to_have_count(1)
                await expect(cell).to_have_attribute('data-available', 'true' if table['id'] in slot['available_table_ids'] else 'false')
            for pair in r.get('combinable', []):
                cell = page.get_by_test_id('slot-' + '+'.join(pair) + '-' + local)
                available = any(x['table_ids'] == pair for x in slot['available_options'])
                if available:
                    await expect(cell).to_have_count(1)
                    await expect(cell).to_have_attribute('data-available', 'true')
                elif await cell.count():
                    await expect(cell).to_have_attribute('data-available', 'false')

    async def screenshot(self, page, name):
        await page.screenshot(path=str(self.out / (name + '.png')), full_page=True,
                              mask=[page.locator('input[type=password]')])

    async def visual(self, page, name):
        metrics = await page.evaluate('''() => {
          const visible=e=>e.getBoundingClientRect().width>0 && e.getBoundingClientRect().height>0;
          const inputs=[...document.querySelectorAll('input,select,textarea')].filter(visible);
          const labels=inputs.map(e=>({hook:e.dataset.testid||'', labelled:[...(e.labels||[])].some(visible)||
            (e.getAttribute('aria-labelledby')||'').split(/\\s+/).some(id=>{const l=document.getElementById(id);return l&&visible(l)})}));
          const rgba=s=>{const a=(s.match(/[\\d.]+/g)||[]).map(Number);return a.length>=3?[a[0],a[1],a[2],a.length>3?a[3]:1]:[0,0,0,0]};
          const composite=(a,b)=>a.slice(0,3).map((v,i)=>v*a[3]+b[i]*(1-a[3]));
          const luminance=a=>a.map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4})
            .reduce((s,v,i)=>s+v*[.2126,.7152,.0722][i],0);
          const contrast=e=>{let bg=[255,255,255],parents=[];for(let p=e;p;p=p.parentElement)parents.unshift(p);
            for(const p of parents)bg=composite(rgba(getComputedStyle(p).backgroundColor),bg);
            const fg=composite(rgba(getComputedStyle(e).color),bg);const a=luminance(fg),b=luminance(bg);
            return (Math.max(a,b)+.05)/(Math.min(a,b)+.05)};
          const states=[...document.querySelectorAll('[data-testid]')].filter(visible).map(e=>({
            hook:e.dataset.testid, colour:getComputedStyle(e).color, background:getComputedStyle(e).backgroundColor,
            border:getComputedStyle(e).borderColor, weight:getComputedStyle(e).fontWeight,
            fontSize:getComputedStyle(e).fontSize,contrast:contrast(e)}));
          return {width:innerWidth,scroll:document.documentElement.scrollWidth,labels,states};
        }''')
        check(metrics['scroll'] <= metrics['width'], 'horizontal page overflow')
        # Associated-label metrics support the required visual review. A visible
        # unassociated label is not silently converted into a new contract rule.
        self.visual_metrics.append({'screen': name, **metrics})
        await self.screenshot(page, name)

    async def routes_auth_grid(self):
        for width in (375, 1280):
            context, page, traffic, fx = await self.fresh(width)
            for path in ('/', '/signup', '/login', '/lookup'):
                response = await page.goto(self.origin + path, wait_until='domcontentloaded')
                check(response.status == 200 and 'text/html' in response.headers.get('content-type', ''), 'screen route not HTML')
                await self.visual(page, 'route-' + (path.strip('/') or 'home') + '-' + str(width))
            await page.goto(self.origin + '/')
            await self.search(page, 6)
            await self.grid(page, fx, 6)
            unavailable = page.get_by_test_id('slot-z-18:00')
            await unavailable.click(force=True)
            check(await page.get_by_test_id('booking-form').count() == 0, 'unavailable cell opened form')
            await page.get_by_test_id('slot-a+z-18:00').click()
            check(urlsplit(page.url).path == '/login' or await page.get_by_test_id('auth-error').count() > 0,
                  'guest selection did not require auth')
            check(not traffic.bookings, 'anonymous browser submitted reservation')
            await self.login(page)
            for path in ('/', '/signup', '/login', '/lookup'):
                await page.goto(self.origin + path)
                await expect(page.get_by_test_id('current-user')).to_contain_text('ada')
            await page.get_by_test_id('logout-button').click()
            check(await page.get_by_test_id('current-user').count() == 0, 'logout retained current-user')
            check(not traffic.blocked_hosts, 'runtime attempted external assets')
            await context.close()

    async def success_retry_lookup(self):
        for ids, party in ((('z',), 2), (('a', 'z'), 6)):
            context, page, traffic, fx = await self.fresh(375)
            await self.login(page); await self.search(page, party); await self.select(page, ids)
            await expect(page.get_by_test_id('booking-party-size')).to_have_value(str(party))
            labels = {t['id']: t['label'] for t in fx['restaurants'][0]['tables']}
            for member in ids:
                await expect(page.get_by_test_id('booking-summary')).to_contain_text(labels[member])
            await expect(page.get_by_test_id('booking-summary')).to_contain_text('18:00')
            await page.get_by_test_id('booking-submit').click()
            await expect(page.get_by_test_id('confirmation')).to_be_visible()
            ref = (await page.get_by_test_id('confirmation-reference').inner_text()).strip()
            check(re.fullmatch('[A-Z0-9]{6,12}', ref) is not None, 'confirmation reference text')
            await expect(page.get_by_test_id('booking-form')).to_be_visible()
            await page.get_by_test_id('booking-submit').click()
            await expect(page.get_by_test_id('confirmation-reference')).to_have_text(ref)
            check(len(traffic.bookings) == 2 and traffic.bookings[0] == traffic.bookings[1], 'successful retry identity changed')
            token = traffic.bookings[-1]['authorization'].removeprefix('Bearer ')
            rows = await self.call(self.api.reservations, token)
            check(len(rows) == 1, 'unchanged success duplicated booking')
            for member in ids:
                await expect(page.get_by_test_id('confirmation-details')).to_contain_text(labels[member])
                await expect(page.get_by_test_id('confirmation-tables')).to_contain_text(labels[member])
            await self.visual(page, 'success-' + ('pair' if len(ids) == 2 else 'single'))
            await self.select(page, ids, '20:00')
            await page.get_by_test_id('booking-submit').click()
            await expect(page.get_by_test_id('confirmation-reference')).not_to_have_text(ref)
            check(traffic.bookings[-1]['key'] != traffic.bookings[-2]['key'], 'changed form reused key')
            await page.goto(self.origin + '/lookup')
            await page.get_by_test_id('lookup-reference-input').fill(ref)
            await page.get_by_test_id('lookup-submit').click()
            await expect(page.get_by_test_id('reservation-status')).to_have_text('confirmed')
            for member in ids:
                await expect(page.get_by_test_id('reservation-tables')).to_contain_text(labels[member])
            await page.get_by_test_id('reservation-cancel-button').click()
            await expect(page.get_by_test_id('reservation-status')).to_have_text('cancelled')
            check(await page.get_by_test_id('reservation-cancel-button').count() == 0, 'cancelled record has cancel button')
            await page.get_by_test_id('lookup-reference-input').fill('ABSENT1')
            await page.get_by_test_id('lookup-submit').click()
            await expect(page.get_by_test_id('reservation-error')).to_be_visible()
            check(await page.get_by_test_id('reservation-detail').count() == 0, 'unknown lookup shows stale detail')
            await context.close()

    async def conflict_preserves_form(self):
        for ids, party in ((('z',), 2), (('a', 'z'), 6)):
            context, page, traffic, fx = await self.fresh()
            await self.login(page); await self.search(page, party); await self.select(page, ids)
            summary = await page.get_by_test_id('booking-summary').inner_text()
            await page.get_by_test_id('booking-party-size').fill(str(party))
            other = await self.call(self.api.login, 'bob')
            await self.call(self.api.book, other, prior.body('z'), 'other-takes-member')
            await page.get_by_test_id('booking-submit').click()
            await expect(page.get_by_test_id('booking-error')).to_be_visible()
            await expect(page.get_by_test_id('booking-form')).to_be_visible()
            await expect(page.get_by_test_id('booking-party-size')).to_have_value(str(party))
            await expect(page.get_by_test_id('booking-summary')).to_have_text(summary)
            check(await page.get_by_test_id('confirmation').count() == 0, 'conflict shows confirmation')
            await expect(page.get_by_test_id('slot-z-18:00')).to_have_attribute('data-available', 'false')
            await self.visual(page, 'conflict-' + ('pair' if len(ids) == 2 else 'single'))
            await self.select(page, ('m', 'q'))
            await page.get_by_test_id('booking-submit').click()
            await expect(page.get_by_test_id('confirmation')).to_be_visible()
            await context.close()

    async def lost_response_recovery(self):
        for ids, party in ((('z',), 2), (('a', 'z'), 6)):
            for loss in ('before', 'after'):
                context, page, traffic, fx = await self.fresh(375)
                await self.login(page); await self.search(page, party); await self.select(page, ids)
                traffic.loss = loss
                await page.get_by_test_id('booking-submit').click()
                await expect(page.get_by_test_id('booking-uncertain')).to_be_visible()
                check((await page.get_by_test_id('booking-uncertain').inner_text()).strip(), 'empty uncertainty')
                check(await page.get_by_test_id('booking-error').count() == 0 and await page.get_by_test_id('confirmation').count() == 0,
                      'lost response incorrectly error/success')
                await self.visual(page, 'uncertain-' + loss + '-' + ('pair' if len(ids) == 2 else 'single'))
                await page.get_by_test_id('booking-submit').click()
                await expect(page.get_by_test_id('confirmation')).to_be_visible()
                check(traffic.bookings[0] == traffic.bookings[1], 'uncertain retry body/key/user changed')
                if loss == 'after':
                    await expect(page.get_by_test_id('confirmation-reference')).to_have_text(traffic.last_committed['reference'])
                check(await page.get_by_test_id('booking-uncertain').count() == 0 and await page.get_by_test_id('booking-error').count() == 0,
                      'retry leaves uncertainty/error')
                token = traffic.bookings[-1]['authorization'].removeprefix('Bearer ')
                check(len(await self.call(self.api.reservations, token)) == 1, 'lost-response recovery duplicated effect')
                await context.close()

    async def out_of_order_search(self):
        fx = oracle.fixture()
        other = copy.deepcopy(fx['restaurants'][0]); other['id'] = 'other'; other['name'] = 'Blue garden'
        for table in other['tables']:
            table['label'] = 'Blue ' + table['label']
        fx['restaurants'].append(other)
        context, page, traffic, _ = await self.fresh(fx=fx)
        await self.login(page)
        gate = traffic.gate(lambda r: urlsplit(r.url).path == '/availability'
                            and parse_qs(urlsplit(r.url).query).get('restaurant_id') == ['r']
                            and parse_qs(urlsplit(r.url).query).get('party_size') == ['2'])
        await self.search(page, 2)
        await asyncio.wait_for(gate['started'].wait(), 10)
        await self.search(page, 7, restaurant='other')
        await self.grid(page, fx, 7, restaurant='other')
        await self.select(page, ('m', 'q'))
        await expect(page.get_by_test_id('booking-summary')).to_contain_text('Blue')
        await expect(page.get_by_test_id('booking-party-size')).to_have_value('7')
        gate['release'].set(); await asyncio.wait_for(gate['finished'].wait(), 10)
        await self.grid(page, fx, 7, restaurant='other')
        await expect(page.get_by_test_id('booking-summary')).to_contain_text('Blue')
        await page.get_by_test_id('booking-submit').click()
        await expect(page.get_by_test_id('confirmation')).to_be_visible()
        check(traffic.bookings[-1]['body']['restaurant_id'] == 'other' and traffic.bookings[-1]['body']['party_size'] == 7,
              'late response corrupted submitted intent')
        await context.close()

    async def signup_keyboard_empty_refused(self):
        context, page, traffic, fx = await self.fresh(375)
        await page.goto(self.origin + '/signup')
        email = 'signup-' + secrets.token_hex(4) + '@verifier.invalid'
        await page.get_by_test_id('signup-email').fill(email)
        await page.get_by_test_id('signup-password').fill(prior.PASSWORD)
        await page.get_by_test_id('signup-display-name').fill('Verification diner')
        await page.get_by_test_id('signup-submit').focus()
        await page.keyboard.press('Enter')
        await expect(page.get_by_test_id('current-user')).to_contain_text('Verification diner')
        check(await page.get_by_test_id('auth-error').count() == 0, 'signup left auth error')
        await page.get_by_test_id('logout-button').click()
        await page.goto(self.origin + '/login')
        await page.get_by_test_id('login-email').fill(email)
        await page.get_by_test_id('login-password').fill(prior.PASSWORD + 'x')
        await page.get_by_test_id('login-submit').click()
        await expect(page.get_by_test_id('auth-error')).to_be_visible()
        await self.visual(page, 'authentication-error-mobile')
        await page.get_by_test_id('login-password').fill(prior.PASSWORD)
        await page.get_by_test_id('login-submit').click()
        await expect(page.get_by_test_id('current-user')).to_contain_text('Verification diner')
        await page.goto(self.origin + '/')
        await self.search(page, 2); await self.select(page, ('z',))
        await page.get_by_test_id('booking-submit').focus()
        focus = await page.get_by_test_id('booking-submit').evaluate('''e=>({outline:getComputedStyle(e).outline,
            boxShadow:getComputedStyle(e).boxShadow,border:getComputedStyle(e).borderColor})''')
        self.visual_metrics.append({'screen': 'keyboard-booking-focus', 'focus': focus})
        await self.screenshot(page, 'keyboard-booking-focus')
        await page.keyboard.press('Enter')
        await expect(page.get_by_test_id('confirmation')).to_be_visible()
        token = traffic.bookings[-1]['authorization'].removeprefix('Bearer ')
        past = await self.call(self.api.book, token, prior.body('m', day='2020-06-06'), 'cutoff-refusal')
        await page.goto(self.origin + '/lookup')
        await page.get_by_test_id('lookup-reference-input').fill(past['reference'])
        await page.get_by_test_id('lookup-submit').click()
        await expect(page.get_by_test_id('reservation-status')).to_have_text('confirmed')
        await page.get_by_test_id('reservation-cancel-button').click()
        await expect(page.get_by_test_id('reservation-error')).to_be_visible()
        await expect(page.get_by_test_id('reservation-status')).to_have_text('confirmed')
        await self.visual(page, 'cutoff-refusal-mobile')
        empty = oracle.fixture(); empty['restaurants'][0]['opening_hours'] = []
        await self.call(self.api.reset, empty)
        await page.goto(self.origin + '/')
        await self.search(page, 2)
        await self.grid(page, empty, 2)
        await self.visual(page, 'closed-day-mobile')
        await context.close()

    async def same_tab_upgrade(self):
        check(self.legacy is not None and self.control is not None, 'browser upgrade needs accepted source and control')
        fx = prior.fixture()
        await self.call(self.legacy.reset, fx)
        context = await self.browser.new_context(viewport={'width': 375, 'height': 900})
        context.set_default_timeout(10000)
        traffic = Traffic(self.origin)
        self.traffics.append(traffic)
        traffic.api_target = self.legacy.url
        # Emulate a retained legacy-single transport; keep this same transformation
        # on both sides. Client body/key AND effective server body/key must be identical.
        traffic.legacy_single_bridge = True
        await context.route('**/*', traffic.handler)
        page = await context.new_page()
        await self.login(page)
        await self.search(page, 2); await self.select(page, ('z',))
        traffic.loss = 'after'
        await page.get_by_test_id('booking-submit').click()
        await expect(page.get_by_test_id('booking-uncertain')).to_be_visible()
        old = traffic.last_committed
        check(old['table_id'] == 'z' and old.get('table_ids', ['z']) == ['z'],
              'immutable accepted Stage1/2/3 source must supply its genuine original single receipt')
        await page.wait_for_load_state('networkidle')
        snapshot = await self.call(self.legacy.expect, 200, 'GET', '/_test/export')
        (self.control / 'browser-pause-legacy').write_text('ready\n')
        deadline = time.monotonic() + 30
        while not (self.control / 'browser-legacy-unavailable').exists():
            if time.monotonic() > deadline:
                raise OSError('browser legacy source-unavailability handshake')
            await asyncio.sleep(.1)
        await self.call(self.destination.expect, 204, 'POST', '/_test/import', snapshot)
        traffic.api_target = self.destination.url
        # No reload, navigation or new page between loss and retry.
        await expect(page.get_by_test_id('current-user')).to_contain_text('ada')
        await expect(page.get_by_test_id('booking-form')).to_be_visible()
        await page.get_by_test_id('booking-submit').click()
        await expect(page.get_by_test_id('confirmation-reference')).to_have_text(old['reference'])
        check(traffic.bookings[0] == traffic.bookings[1], 'same-tab upgraded retry identity changed')
        check(await page.get_by_test_id('booking-uncertain').count() == 0, 'legacy recovery stays uncertain')
        await expect(page.get_by_test_id('confirmation-details')).to_contain_text('Z')
        await page.goto(self.origin + '/lookup')
        await page.get_by_test_id('lookup-reference-input').fill(old['reference'])
        await page.get_by_test_id('lookup-submit').click()
        await expect(page.get_by_test_id('reservation-status')).to_have_text('confirmed')
        await expect(page.get_by_test_id('reservation-tables')).to_contain_text('Z')
        await context.close()

    async def submitted_user_race(self):
        context, page, traffic, fx = await self.fresh()
        await self.login(page); await self.search(page, 6); await self.select(page, ('a', 'z'))
        gate = traffic.gate(lambda r: urlsplit(r.url).path == '/reservations' and r.method == 'POST')
        await page.get_by_test_id('booking-submit').click()
        await asyncio.wait_for(gate['started'].wait(), 10)
        await page.get_by_test_id('logout-button').click()
        await self.login(page, 'bob')
        gate['release'].set(); await asyncio.wait_for(gate['finished'].wait(), 10)
        await expect(page.get_by_test_id('current-user')).to_contain_text('bob')
        check(await page.get_by_test_id('confirmation').count() == 0, 'old-user late response leaked confirmation')
        await self.search(page, 6); await self.select(page, ('m', 'q'))
        await page.get_by_test_id('booking-submit').click()
        await expect(page.get_by_test_id('confirmation')).to_be_visible()
        check(traffic.bookings[-1]['authorization'] != traffic.bookings[0]['authorization'], 'submitted intent reused previous user')
        await context.close()

    async def pair_same_tab_import(self):
        check(self.control is not None, 'pair continuity requires source control')
        context, page, traffic, fx = await self.fresh(375)
        await self.login(page); await self.search(page, 6); await self.select(page, ('a', 'z'))
        traffic.loss = 'after'
        await page.get_by_test_id('booking-submit').click()
        await expect(page.get_by_test_id('booking-uncertain')).to_be_visible()
        original = traffic.last_committed
        await page.wait_for_load_state('networkidle')
        snapshot = await self.call(self.api.expect, 200, 'GET', '/_test/export')
        (self.control / 'browser-pause-source').write_text('ready\n')
        deadline = time.monotonic() + 30
        while not (self.control / 'browser-source-unavailable').exists():
            if time.monotonic() > deadline:
                raise OSError('browser pair source-unavailability handshake')
            await asyncio.sleep(.1)
        await self.call(self.destination.expect, 204, 'POST', '/_test/import', snapshot)
        traffic.api_target = traffic.assets_target = self.destination.url
        await expect(page.get_by_test_id('booking-form')).to_be_visible()
        await expect(page.get_by_test_id('current-user')).to_contain_text('ada')
        await page.get_by_test_id('booking-submit').click()
        await expect(page.get_by_test_id('confirmation-reference')).to_have_text(original['reference'])
        check(traffic.bookings[0] == traffic.bookings[1], 'pair imported retry body/key/user changed')
        check(await page.get_by_test_id('booking-uncertain').count() == 0, 'pair recovered receipt remains uncertain')
        for table in fx['restaurants'][0]['tables']:
            if table['id'] in original['table_ids']:
                await expect(page.get_by_test_id('confirmation-tables')).to_contain_text(table['label'])
        await context.close()

    async def run(self, selected=None):
        names = ['routes_auth_grid', 'signup_keyboard_empty_refused', 'success_retry_lookup', 'conflict_preserves_form', 'lost_response_recovery',
                 'out_of_order_search', 'submitted_user_race', 'same_tab_upgrade', 'pair_same_tab_import']
        for name in selected or names:
            check(name in names, 'unknown browser case')
            started = time.monotonic()
            try:
                await getattr(self, name)()
                result = {'case': name, 'status': 'PASS'}
            except prior.CheckFailure as exc:
                result = {'case': name, 'status': 'FAIL', 'classification': 'PRODUCT DEFECT', 'detail': str(exc)}
            except AssertionError:
                result = {'case': name, 'status': 'FAIL', 'classification': 'PRODUCT DEFECT', 'detail': 'browser assertion; inspect sanitized screenshot'}
            except Exception as exc:
                result = {'case': name, 'status': 'ERROR', 'classification': 'INCONCLUSIVE', 'detail': type(exc).__name__}
            finally:
                for traffic in self.traffics:
                    if traffic.delayed:
                        traffic.delayed['release'].set()
                for context in list(self.browser.contexts):
                    await context.close()
            result['seconds'] = round(time.monotonic() - started, 3)
            self.results.append(result)
            print(json.dumps(result), flush=True)
        return {'campaign': 'independent-stage-2-browser', 'cases': self.results,
                'all_passed': all(x['status'] == 'PASS' for x in self.results),
                'visual_review_required': True, 'visual_metrics': self.visual_metrics}


async def calibrate(browser, out):
    page = await browser.new_page(viewport={'width': 375, 'height': 700})
    await page.set_content('<label for="party">Guests</label><input id="party" data-testid="party-size-input"><button data-testid="booking-submit">Reserve</button>')
    await expect(page.get_by_test_id('party-size-input')).to_be_visible()
    await page.keyboard.press('Tab')
    check(await page.get_by_test_id('party-size-input').evaluate('(e)=>e===document.activeElement'), 'keyboard calibration')
    controls = BrowserCampaign(browser, 'http://verifier.invalid', None, None, out)
    await controls.visual(page, 'controlled-calibration')
    check(all(x['labelled'] for x in controls.visual_metrics[0]['labels']), 'label metric calibration')
    check(all(x['contrast'] > 0 for x in controls.visual_metrics[0]['states']), 'contrast metric calibration')
    await page.close()
    return {'browser_calibration': 'PASS', 'production_executed': False, 'controlled_DOM_only': True}


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['calibrate', 'http'])
    parser.add_argument('--revision'); parser.add_argument('--released', action='store_true')
    parser.add_argument('--source'); parser.add_argument('--destination'); parser.add_argument('--legacy')
    parser.add_argument('--control'); parser.add_argument('--out', required=True); parser.add_argument('--cases', nargs='+')
    args = parser.parse_args()
    if args.mode == 'http' and (not args.released or not re.fullmatch('[0-9a-f]{40}', args.revision or '')):
        parser.error('Conductor integrated full exact-SHA release required')
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        if args.mode == 'calibrate':
            report = await calibrate(browser, out)
        else:
            report = await BrowserCampaign(browser, args.source, args.destination, args.legacy, out, args.control).run(args.cases)
            report['production_revision'] = args.revision
        await browser.close()
    (out / 'browser-summary.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'visual_metrics'}))
    raise SystemExit(0 if report.get('all_passed', report.get('browser_calibration') == 'PASS') else 1)


if __name__ == '__main__':
    asyncio.run(main())
