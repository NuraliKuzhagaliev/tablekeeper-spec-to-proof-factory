"""Independent real-browser optional disclosure and selected-policy scenarios."""
import argparse
import asyncio
import json
from pathlib import Path
import re
import time
from urllib.parse import urlsplit

from playwright.async_api import async_playwright, expect
import stage3_campaign as core
import policy_oracle as model
import stage1_campaign as prior
import browser_campaign as old

check = prior.check


class Traffic(old.Traffic):
    def __init__(self, origin):
        super().__init__(origin)
        self.gates = []; self.faults = {}; self.active = set(); self.closing = False

    def hold(self, suffix):
        gate = {'suffix': suffix, 'started': asyncio.Event(), 'release': asyncio.Event(), 'finished': asyncio.Event()}
        self.gates.append(gate); return gate

    async def handler(self, route):
        task = asyncio.current_task(); self.active.add(task)
        try:
            await self.handle(route)
        except Exception:
            if not self.closing and not route.request.failure:
                raise
        finally:
            self.active.discard(task)

    async def handle(self, route):
        path = urlsplit(route.request.url).path
        if path.endswith('/history') or path.endswith('/decision'):
            fault = self.faults.pop(path.rsplit('/', 1)[-1], None)
            if fault == 'network':
                await route.abort('failed'); return
            if fault == '404':
                await route.fulfill(status=404, content_type='application/json; charset=utf-8',
                                    json={'error': {'code': 'not_found', 'message': 'Synthetic contained optional-read failure'}}); return
            response = await route.fetch(url=self.api_target + path, timeout=5000)
            body = await response.body(); headers = response.headers; status = response.status
            if fault == 'unreadable':
                body = b'not-json'
            if fault == 'revision':
                parsed = json.loads(body); parsed['revision'] += 1; body = json.dumps(parsed).encode()
            gate = next((g for g in self.gates if path.endswith(g['suffix']) and not g['started'].is_set()), None)
            if gate:
                gate['started'].set(); await gate['release'].wait()
            try:
                await route.fulfill(status=status, headers=headers, body=body)
            except Exception:
                if not route.request.failure:
                    raise
            finally:
                if gate:
                    gate['finished'].set()
            return
        await super().handler(route)


class Browser(old.BrowserCampaign):
    async def close_context(self, context, traffic):
        traffic.closing = True
        for gate in traffic.gates:
            gate['release'].set()
        if traffic.active:
            try:
                await asyncio.wait_for(asyncio.gather(*list(traffic.active), return_exceptions=True), 10)
            except TimeoutError:
                pass
        await context.close()

    async def setup(self, width=1280):
        old.Traffic = Traffic
        context, page, traffic, fx = await self.fresh(width, model.fixture())
        page.on('pageerror', lambda e: self.errors.append(type(e).__name__))
        await self.login(page)
        token = await self.call(self.api.login)
        return context, page, traffic, fx, token

    async def lookup(self, page, ref, navigate=True):
        if navigate:
            await page.goto(self.origin + '/lookup', wait_until='domcontentloaded')
        await page.get_by_test_id('lookup-reference-input').fill(ref)
        await page.get_by_test_id('lookup-submit').click()
        await expect(page.get_by_test_id('reservation-detail')).to_be_visible()
        await expect(page.get_by_test_id('reservation-detail')).to_contain_text(ref)

    async def open_story(self, page):
        disclosure = page.get_by_test_id('provenance-disclosure')
        await expect(disclosure).to_be_visible()
        await disclosure.locator('summary').click()

    async def create(self, token, table='z', key='one', day=prior.DAY):
        return await self.call(self.api.book, token, prior.body(table, day=day), key)

    async def native_terms_history_visual(self):
        for width in [375, 1280]:
            context, page, traffic, fx, token = await self.setup(width)
            r = fx['restaurants'][0]
            anchor = await self.call(self.api.book, token, {'restaurant_id': 'r', 'table_ids': ['z', 'a'],
                'starts_at_local': prior.DAY + 'T18:00', 'party_size': 6}, 'native-pair')
            p = model.policy(r, prior.DAY, reservation_duration_minutes=120, cancellation_cutoff_minutes=60)
            await self.call(self.api.expect, 201, 'POST', '/restaurants/r/policies', p, token, 'publication')
            changed = await self.call(self.api.expect, 200, 'PATCH', '/reservations/' + anchor['reference'],
                                      {'party_size': 5, 'starts_at_local': prior.DAY + 'T18:30'}, token)
            await self.lookup(page, anchor['reference']); await self.open_story(page)
            await expect(page.get_by_test_id('reservation-history')).to_be_visible()
            await expect(page.get_by_test_id('accepted-terms')).to_contain_text('120 minutes')
            events = page.get_by_test_id('history-event')
            await expect(events).to_have_count(2)
            check(await events.evaluate_all('(es)=>es.map(e=>Number(e.dataset.seq))') == [1, 2], 'rendered history sequence order')
            await events.nth(0).get_by_test_id('event-terms').locator(':scope > summary').click()
            await expect(events.nth(0).get_by_test_id('event-terms')).to_contain_text('90 minutes')
            for label in ['Window alcove', 'Courtyard bench']:
                await expect(page.get_by_test_id('reservation-detail')).to_contain_text(label)
                await expect(events.nth(0)).to_contain_text(label)
            await expect(events.nth(1)).to_contain_text('18:30')
            await page.get_by_test_id('accepted-terms').locator('details summary').click()
            await expect(page.get_by_test_id('accepted-terms')).to_contain_text('Chef’s nook')
            await self.visual(page, 'independent-native-story-' + str(width))
            await page.get_by_test_id('reservation-cancel-button').click()
            await expect(page.get_by_test_id('reservation-status')).to_have_text('cancelled')
            await expect(page.get_by_test_id('history-event')).to_have_count(3)
            await expect(page.get_by_test_id('history-event').nth(2)).to_contain_text('cancelled')
            check(await page.get_by_test_id('reservation-cancel-button').count() == 0, 'story cancel left required cancel button')
            await self.visual(page, 'independent-cancelled-story-' + str(width))
            check(not traffic.blocked_hosts, 'optional story external asset dependency')
            await self.close_context(context, traffic)

    async def contained_partial_and_mismatch_failures(self):
        for side, fault in [('history', 'network'), ('decision', '404'), ('history', 'unreadable'), ('decision', 'revision')]:
            context, page, traffic, fx, token = await self.setup(375)
            row = await self.create(token)
            await self.lookup(page, row['reference']); traffic.faults[side] = fault
            await self.open_story(page)
            await expect(page.get_by_test_id('provenance-error')).to_be_visible()
            check(bool((await page.get_by_test_id('provenance-error').inner_text()).strip()), 'empty optional-read feedback')
            await expect(page.get_by_test_id('reservation-status')).to_have_text('confirmed')
            await expect(page.get_by_test_id('reservation-cancel-button')).to_be_enabled()
            if fault == 'revision':
                check(await page.get_by_test_id('accepted-terms').count() == 0 and await page.get_by_test_id('reservation-history').count() == 0,
                      'mismatched snapshots presented together as current')
            await page.get_by_test_id('provenance-refresh').click()
            await expect(page.get_by_test_id('reservation-history')).to_be_visible()
            await expect(page.get_by_test_id('accepted-terms')).to_be_visible()
            check(await page.get_by_test_id('provenance-error').count() == 0, 'optional retry error remains')
            await page.get_by_test_id('reservation-cancel-button').click()
            await expect(page.get_by_test_id('reservation-status')).to_have_text('cancelled')
            await self.close_context(context, traffic)

    async def crossed_reference_and_cancel_reads(self):
        for suffix in ['/history', '/decision']:
            context, page, traffic, fx, token = await self.setup()
            one = await self.create(token); two = await self.create(token, 'm', 'two')
            await self.lookup(page, one['reference']); gate = traffic.hold(suffix); await self.open_story(page)
            await asyncio.wait_for(gate['started'].wait(), 10)
            await self.lookup(page, two['reference'], navigate=False)
            if not await page.get_by_test_id('provenance-disclosure').evaluate('(e)=>e.open'):
                await self.open_story(page)
            await expect(page.get_by_test_id('reservation-history')).to_be_visible()
            gate['release'].set(); await asyncio.wait_for(gate['finished'].wait(), 10)
            await expect(page.get_by_test_id('reservation-detail')).to_contain_text(two['reference'])
            await expect(page.get_by_test_id('reservation-detail')).to_contain_text('Chef’s nook')
            check('Window alcove' not in await page.get_by_test_id('reservation-history').inner_text(), 'late story restored other reference')
            gate = traffic.hold(suffix); await page.get_by_test_id('provenance-refresh').click()
            await asyncio.wait_for(gate['started'].wait(), 10)
            await page.get_by_test_id('reservation-cancel-button').click()
            await expect(page.get_by_test_id('reservation-status')).to_have_text('cancelled')
            gate['release'].set(); await asyncio.wait_for(gate['finished'].wait(), 10)
            await expect(page.get_by_test_id('history-event')).to_have_count(2)
            await expect(page.get_by_test_id('history-event').nth(1)).to_contain_text('cancelled')
            await self.close_context(context, traffic)

    async def late_reads_after_user_or_navigation(self):
        for action in ['logout', 'navigation', 'switchuser']:
            context, page, traffic, fx, token = await self.setup()
            row = await self.create(token)
            await self.lookup(page, row['reference']); gate = traffic.hold('/history'); await self.open_story(page)
            await asyncio.wait_for(gate['started'].wait(), 10)
            if action in ['logout', 'switchuser']:
                await page.get_by_test_id('logout-button').click()
                if action == 'switchuser':
                    await self.login(page, 'bob')
            else:
                await page.locator('a[data-nav][href="/"]').first.click()
                await expect(page.get_by_test_id('restaurant-select')).to_be_visible()
            gate['release'].set(); await asyncio.wait_for(gate['finished'].wait(), 10)
            check(await page.get_by_test_id('reservation-history').count() == 0 and await page.get_by_test_id('accepted-terms').count() == 0,
                  'private story resurrected after user/navigation change')
            if action == 'logout':
                check(await page.get_by_test_id('current-user').count() == 0, 'late private read restored session')
            if action == 'switchuser':
                await expect(page.get_by_test_id('current-user')).to_contain_text('bob')
            await self.close_context(context, traffic)

    async def fixture_and_legacy_known_state(self):
        context, page, traffic, fx, token = await self.setup(375)
        fixture = model.fixture()
        fixture['reservations'] = [dict(prior.body(), id='fixture-cancelled', reference='FIXCAN', user_id='ada', status='cancelled')]
        # Re-login after replacing state, so required session remains authoritative.
        await self.call(self.api.reset, fixture)
        await page.get_by_test_id('logout-button').click()
        await self.login(page)
        await self.lookup(page, 'FIXCAN'); await self.open_story(page)
        await expect(page.get_by_test_id('history-baseline')).to_be_visible()
        await expect(page.get_by_test_id('history-empty')).to_be_visible()
        check(await page.get_by_test_id('history-event').count() == 0, 'cancelled fixture invented event history')
        await expect(page.get_by_test_id('history-baseline')).to_contain_text('cancelled')
        await self.visual(page, 'independent-fixture-baseline-375')
        await self.close_context(context, traffic)
        if self.legacy:
            context, page, traffic, fx, token = await self.setup(375)
            await self.call(self.legacy.reset, fx); old_token = await self.call(self.legacy.login)
            old_row = await self.call(self.legacy.book, old_token, prior.body(), 'old-original')
            await self.call(self.legacy.expect, 200, 'PATCH', '/reservations/' + old_row['reference'], {'table_id': 'm'}, old_token)
            snapshot = await self.call(self.legacy.expect, 200, 'GET', '/_test/export')
            await self.call(self.api.expect, 204, 'POST', '/_test/import', snapshot)
            # Authentication against imported account uses its original hash.
            await page.get_by_test_id('logout-button').click()
            await self.login(page)
            await self.lookup(page, old_row['reference']); await self.open_story(page)
            await expect(page.get_by_test_id('history-baseline')).to_contain_text('earlier changes were not recorded', ignore_case=True)
            await expect(page.get_by_test_id('history-empty')).to_be_visible()
            await expect(page.get_by_test_id('history-baseline')).to_contain_text('Chef’s nook')
            check(await page.get_by_test_id('history-event').count() == 0, 'legacy invented historical amendment')
            await page.get_by_test_id('reservation-cancel-button').click()
            await expect(page.get_by_test_id('history-event')).to_have_count(1)
            await expect(page.get_by_test_id('history-event')).to_have_attribute('data-seq', '1')
            await expect(page.get_by_test_id('history-event')).to_contain_text('cancelled')
            await self.close_context(context, traffic)

    async def selected_policy_search_and_keyboard(self):
        context, page, traffic, fx, token = await self.setup(375)
        policy = model.policy(fx['restaurants'][0], prior.DAY, slot_minutes=60, reservation_duration_minutes=120,
                              capacities={t['id']: 1 for t in fx['restaurants'][0]['tables']})
        await self.call(self.api.expect, 201, 'POST', '/restaurants/r/policies', policy, token, 'current-search')
        await self.search(page, 2)
        await expect(page.get_by_test_id('availability-grid')).to_be_visible()
        await expect(page.get_by_test_id('slot-z-18:00')).to_have_attribute('data-available', 'false')
        pair = page.get_by_test_id('slot-a+z-18:00')
        await expect(pair).to_have_attribute('data-available', 'true')
        check(await page.get_by_test_id('slot-z-18:30').count() == 0, 'browser used original detail grid instead of selected policy')
        await pair.focus(); await page.keyboard.press('Enter')
        await expect(page.get_by_test_id('booking-form')).to_be_visible()
        focused = await page.evaluate('''()=>{const e=document.activeElement,s=getComputedStyle(e);return {outline:s.outlineStyle,width:s.outlineWidth,shadow:s.boxShadow}}''')
        check(focused['outline'] != 'none' or focused['shadow'] != 'none', 'keyboard selection loses visible focus')
        await self.visual(page, 'independent-policy-pair-form-375')
        await page.get_by_test_id('booking-submit').click()
        await expect(page.get_by_test_id('confirmation')).to_be_visible()
        await self.visual(page, 'independent-policy-pair-confirmation-375')
        check(not traffic.blocked_hosts, 'selected-policy browser external assets')
        await self.close_context(context, traffic)


CASES = ['native_terms_history_visual', 'contained_partial_and_mismatch_failures', 'crossed_reference_and_cancel_reads',
         'late_reads_after_user_or_navigation', 'fixture_and_legacy_known_state', 'selected_policy_search_and_keyboard']


async def main():
    p = argparse.ArgumentParser(); p.add_argument('--released', action='store_true'); p.add_argument('--revision', required=True)
    for name in ['source', 'destination', 'legacy', 'control', 'out']:
        p.add_argument('--' + name)
    p.add_argument('--cases', nargs='+'); args = p.parse_args()
    if not args.released or not re.fullmatch('[0-9a-f]{40}', args.revision):
        p.error('explicit FULL Stage 3 release required')
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        checks = Browser(browser, args.source, args.destination, args.legacy, out, args.control); checks.errors = []
        results = []
        for name in args.cases or CASES:
            started = time.monotonic()
            try:
                await getattr(checks, name)(); result = {'case': name, 'status': 'PASS'}
            except Exception as error:
                result = {'case': name, 'status': 'ERROR', 'classification': 'INCONCLUSIVE', 'detail': type(error).__name__,
                          'message': str(error)[:300]}
            finally:
                for traffic in checks.traffics:
                    traffic.closing = True
                    for gate in getattr(traffic, 'gates', []):
                        gate['release'].set()
                    if traffic.active:
                        try:
                            await asyncio.wait_for(asyncio.gather(*list(traffic.active), return_exceptions=True), 10)
                        except TimeoutError:
                            pass
                for context in list(browser.contexts):
                    await context.close()
            result['seconds'] = round(time.monotonic() - started, 3); results.append(result)
            print(json.dumps(result), flush=True)
        await browser.close()
    report = {'production_revision': args.revision, 'cases': results, 'all_passed': all(x['status'] == 'PASS' for x in results),
              'page_errors': checks.errors, 'visual_metrics': checks.visual_metrics, 'visual_review_required': True}
    (out / 'disclosure-summary.json').write_text(json.dumps(report, indent=2) + '\n')
    raise SystemExit(0 if report['all_passed'] else 1)


if __name__ == '__main__':
    asyncio.run(main())
