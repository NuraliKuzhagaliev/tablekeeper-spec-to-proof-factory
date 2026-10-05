#!/usr/bin/env python3
"""Remaining explicit ledger protocols; same pinned revision and independent models."""
import argparse
import asyncio
import copy
import json
from pathlib import Path
import re
import time
import traceback
from urllib.parse import urlsplit, parse_qs

from playwright.async_api import async_playwright, expect
import browser_campaign as browser_checks
import campaign as api_checks
import oracle
import stage1_campaign as prior

check = prior.check


class APIExtensions(api_checks.Campaign):
    def pair_exact_sum_snapshot_transfer(self):
        vector = oracle.feasible_capacity_vectors()[-1]
        fx = oracle.fixture(zone='UTC')
        fx['restaurants'][0]['tables'][0]['capacity'] = vector['left']
        fx['restaurants'][0]['tables'][1]['capacity'] = vector['right']
        a, token = self.fresh(fx)
        second_token = a.login()
        body = api_checks.request(party=vector['sum'])
        original = a.book(token, body, 'exact-create')
        moves = {'moves': [{'reference': original['reference'], 'table_ids': ['m', 'q'], 'party_size': 8}]}
        batch = a.expect(201, 'POST', '/reservation-moves', moves, token, 'exact-move')
        a.expect(200, 'POST', '/reservations/' + original['reference'] + '/cancel', token=token)
        failed = api_checks.request(party=vector['sum'] + 1, at='20:00')
        a.book(token, failed, 'exact-failed', 422, 'party_exceeds_capacity')
        records = a.reservations(token)
        snapshot = a.expect(200, 'GET', '/_test/export')
        # Destroy source state after the private snapshot; destination must be
        # independent of subsequent source writes and accounts.
        a.reset(oracle.fixture())
        a.expect(401, 'GET', '/reservations', token=token, code='unauthenticated')
        failed_response = None
        for d in (self.dest, self.third):
            check(d is not None, 'third independent process required')
            d.expect(204, 'POST', '/_test/import', snapshot)
            for session in (token, second_token, d.login()):
                check(d.reservations(session) == records, 'exact pair transfer changed records/session')
            check(d.book(token, body, 'exact-create', 200) == original, 'giant original response rounded/regenerated')
            check(d.expect(200, 'POST', '/reservation-moves', moves, token, 'exact-move') == batch,
                  'numeric historical move receipt changed')
            check(d.slots(party=vector['sum']) == oracle.slots(fx, prior.DAY, vector['sum'], records),
                  'transferred giant pair config/capacity threshold changed')
            recovered = d.book(token, api_checks.request(party=vector['sum'], at='20:00'), 'exact-failed',
                               201 if failed_response is None else 200)
            if failed_response is not None:
                check(recovered == failed_response, 'chained numeric receipt changed')
            failed_response = recovered
            snapshot = d.expect(200, 'GET', '/_test/export')
            records = d.reservations(token)

    def pair_selector_precedence_and_receipts(self):
        a, token = self.fresh()
        row = a.book(token, api_checks.request(), 'create')
        path = '/reservations/' + row['reference']
        for change in ({'table_ids': ['z', 'a']}, {'ignored': 1}):
            check(a.expect(200, 'PATCH', path, change, token) == row, 'semantic pair no-op changed values')
        original = a.expect(201, 'POST', '/reservation-moves',
                            {'moves': [{'reference': row['reference'], 'table_ids': ['a', 'z']}]}, token, 'move')
        a.expect(409, 'POST', '/reservation-moves',
                 {'moves': [{'reference': row['reference'], 'table_ids': ['z', 'a']}]}, token, 'move', 'idempotency_key_reuse')
        before = a.reservations(token)
        for selector, status, code in [({'table_ids': []}, 422, 'validation_failed'),
                                      ({'table_ids': ['a', 'm']}, 422, 'combination_not_allowed'),
                                      ({'table_ids': ['z', 'a', 'm']}, 422, 'combination_not_allowed'),
                                      ({'table_ids': ['a', 'a']}, 422, 'validation_failed'),
                                      ({'table_ids': ['a', 'z'], 'table_id': 'z'}, 422, 'validation_failed'),
                                      ({'table_ids': 'z'}, 400, 'malformed_request'),
                                      ({'table_ids': [True]}, 400, 'malformed_request'),
                                      ({'table_ids': ['missing']}, 404, 'not_found')]:
            a.expect(status, 'PATCH', path, selector, token, code=code)
            a.expect(status, 'POST', '/reservation-moves', {'moves': [{'reference': row['reference'], **selector}]},
                     token, 'failed', code)
            check(a.reservations(token) == before, 'invalid pair selector changed state')
        check(a.expect(201, 'POST', '/reservation-moves', {'moves': [{'reference': row['reference']}]},
                       token, 'failed')['reservations'] == [row], 'failed pair keys not reusable/no-op')
        # An unlisted booking blocks one shared member without touching any other.
        blocker = a.book(token, api_checks.request(('m',), 1), 'blocker')
        before = a.reservations(token)
        a.expect(409, 'PATCH', path, {'table_ids': ['z', 'm']}, token, code='table_unavailable')
        a.expect(409, 'POST', '/reservation-moves', {'moves': [{'reference': row['reference'], 'table_ids': ['z', 'm']}]},
                 token, 'blocked', 'table_unavailable')
        check(a.reservations(token) == before, 'unlisted member conflict partially changed state')
        other = a.login('bob')
        for method, suffix, body in [('GET', '', None), ('POST', '/cancel', None), ('PATCH', '', {'party_size': 1})]:
            a.expect(404, method, path + suffix, body, other, code='not_found')
        a.expect(404, 'POST', '/reservation-moves', {'moves': [{'reference': row['reference']}]}, other, 'foreign', 'not_found')
        a.expect(200, 'POST', path + '/cancel', token=token)
        check(a.expect(200, 'POST', '/reservation-moves',
                       {'moves': [{'reference': row['reference'], 'table_ids': ['a', 'z']}]}, token, 'move') == original,
              'cancelled pair original move receipt changed')
        for method in ('PATCH', 'POST'):
            a.expect(409, method, path if method == 'PATCH' else '/reservation-moves',
                     {'party_size': 1} if method == 'PATCH' else {'moves': [{'reference': row['reference']}]},
                     token, None if method == 'PATCH' else 'cancelled', 'reservation_cancelled')

    def pair_amendment_dst_and_cutoff(self):
        for zone, day, target in [('Europe/Berlin', '2026-03-29', '02:30'),
                                  ('America/New_York', '2026-03-08', '02:30'),
                                  ('Europe/Berlin', '2026-10-25', '02:30'),
                                  ('America/New_York', '2026-11-01', '01:30')]:
            for batch in (False, True):
                fx = oracle.fixture(zone=zone, opens='00:00', closes='05:00')
                a, token = self.fresh(fx)
                row = a.book(token, api_checks.request(at='01:00'), 'future')
                change = {'starts_at_local': day + 'T' + target}
                before = a.reservations(token)
                args = ('POST', '/reservation-moves', {'moves': [{'reference': row['reference'], **change}]}, token, 'dst') if batch else (
                        'PATCH', '/reservations/' + row['reference'], change, token)
                if '-03-' in day:
                    a.expect(422, *args, code='invalid_local_time')
                    check(a.reservations(token) == before, 'skipped-time amendment partially changed pair')
                else:
                    reply = a.expect(201 if batch else 200, *args)
                    current = reply['reservations'][0] if batch else reply
                    start = prior.resolve(change['starts_at_local'], zone)
                    check(current['starts_at'] == start.isoformat(), 'amended pair not first occurrence')
                    check(prior.instant_seconds(current['ends_at']) - prior.instant_seconds(current['starts_at']) == 5400,
                          'amended pair duration not absolute')
                    check(a.slots(day, 1) == oracle.slots(fx, day, 1, [current]), 'amended DST member occupancy')
        a, token = self.fresh()
        past = a.book(token, api_checks.request(day='2020-06-06'), 'past')
        future = a.book(token, api_checks.request(('m', 'q'), 6), 'future')
        before = a.reservations(token)
        invalid = {'moves': [{'reference': past['reference'], 'table_ids': ['a', 'm']},
                             {'reference': future['reference'], 'party_size': False}]}
        a.expect(409, 'POST', '/reservation-moves', invalid, token, 'cutoff', 'cutoff_passed')
        invalid['moves'].reverse()
        a.expect(422, 'POST', '/reservation-moves', invalid, token, 'input-order', 'validation_failed')
        check(a.reservations(token) == before, 'batch input/cutoff precedence changed state')


class ExtendedTraffic(browser_checks.Traffic):
    async def handler(self, route):
        req = route.request
        if self.loss == 'unreadable' and urlsplit(req.url).path == '/reservations' and req.method == 'POST':
            self.loss = None
            body = json.loads(req.post_data)
            headers = await req.all_headers()
            self.bookings.append({'body': body, 'effective_body': copy.deepcopy(body),
                                  'key': headers.get('idempotency-key'), 'authorization': headers.get('authorization')})
            response = await route.fetch(timeout=5000)
            check(response.status == 201, 'unreadable-response setup not committed')
            self.last_committed = await response.json()
            await route.fulfill(status=201, content_type='application/json; charset=utf-8', body='{')
            return
        gate = self.delayed
        if gate and gate['match'](req) and not gate['started'].is_set():
            parsed = urlsplit(req.url)
            if parsed.path == '/reservations' and req.method == 'POST':
                original = json.loads(req.post_data)
                request_headers = await req.all_headers()
                self.bookings.append({'body': original, 'effective_body': copy.deepcopy(original),
                                      'key': request_headers.get('idempotency-key'),
                                      'authorization': request_headers.get('authorization')})
            response = await route.fetch(url=self.api_target + parsed.path + ('?' + parsed.query if parsed.query else ''), timeout=5000)
            # Store bytes before holding the response; Playwright may dispose
            # APIResponse handles when an interrupted case closes its context.
            body, headers, status = await response.body(), response.headers, response.status
            gate['started'].set()
            await gate['release'].wait()
            try:
                await route.fulfill(status=status, headers=headers, body=body)
            except Exception:
                if not req.failure: raise
            finally:
                gate['finished'].set()
            return
        await super().handler(route)


class BrowserExtensions(browser_checks.BrowserCampaign):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.runtime_errors = []

    async def fresh(self, *args, **kwargs):
        context, page, traffic, fx = await super().fresh(*args, **kwargs)
        page.on('pageerror', lambda error: self.runtime_errors.append(type(error).__name__))
        return context, page, traffic, fx

    async def crossed_detail_closed_and_error(self):
        for variant in ('detail', 'closed', 'error'):
            fx = oracle.fixture()
            other = copy.deepcopy(fx['restaurants'][0]); other['id'] = 'other'; other['name'] = 'Blue garden'
            for table in other['tables']:
                table['label'] = 'Blue ' + table['label']
            fx['restaurants'].append(other)
            if variant == 'closed': fx['restaurants'][0]['opening_hours'] = []
            context, page, traffic, _ = await self.fresh(fx=fx)
            await self.login(page)
            if variant == 'error':
                await page.wait_for_load_state('networkidle')
                reduced = copy.deepcopy(fx)
                reduced['restaurants'] = [other]
                await self.call(self.api.reset, reduced)
            gate = traffic.gate(lambda r: urlsplit(r.url).path == ('/restaurants/r' if variant == 'detail' else '/availability')
                                and (variant == 'detail' or parse_qs(urlsplit(r.url).query).get('restaurant_id') == ['r']))
            await self.search(page, 2)
            await asyncio.wait_for(gate['started'].wait(), 10)
            await self.visual(page, 'loading-' + variant)
            await self.search(page, 7, restaurant='other')
            await self.grid(page, fx, 7, restaurant='other'); await self.select(page, ('m', 'q'))
            await expect(page.get_by_test_id('booking-summary')).to_contain_text('Blue')
            gate['release'].set(); await asyncio.wait_for(gate['finished'].wait(), 10)
            await self.grid(page, fx, 7, restaurant='other')
            await expect(page.get_by_test_id('booking-summary')).to_contain_text('Blue')
            await expect(page.get_by_test_id('booking-party-size')).to_have_value('7')
            await context.close()

    async def conflict_refresh_and_frozen_search_intent(self):
        for ids, party in [(('z',), 2), (('a', 'z'), 6)]:
            context, page, traffic, fx = await self.fresh()
            await self.login(page); await self.search(page, party); await self.select(page, ids)
            summary = await page.get_by_test_id('booking-summary').inner_text()
            bob = await self.call(self.api.login, 'bob')
            taken = await self.call(self.api.book, bob, prior.body('z'), 'member')
            gate = traffic.gate(lambda r: urlsplit(r.url).path == '/availability')
            await page.get_by_test_id('booking-submit').click()
            await expect(page.get_by_test_id('booking-error')).to_be_visible()
            await expect(page.get_by_test_id('booking-summary')).to_have_text(summary)
            await expect(page.get_by_test_id('booking-party-size')).to_have_value(str(party))
            await asyncio.wait_for(gate['started'].wait(), 10)
            await self.search(page, 8); await self.grid(page, fx, 8, occupied=[taken]); await self.select(page, ('m', 'q'))
            gate['release'].set(); await asyncio.wait_for(gate['finished'].wait(), 10)
            await self.grid(page, fx, 8, occupied=[taken])
            await expect(page.get_by_test_id('booking-party-size')).to_have_value('8')
            # Typing a different search party cannot retroactively change a
            # selection belonging to the currently displayed query.
            await page.get_by_test_id('party-size-input').fill('1')
            await self.select(page, ('m', 'q'), '20:00')
            await expect(page.get_by_test_id('booking-party-size')).to_have_value('8')
            await page.get_by_test_id('booking-submit').click()
            await expect(page.get_by_test_id('confirmation')).to_be_visible()
            check(traffic.bookings[-1]['body']['party_size'] == 8, 'typed search control corrupted selected query')
            await context.close()

    async def unreadable_and_changed_pending_intent(self):
        for ids, party in [(('z',), 2), (('a', 'z'), 6)]:
            context, page, traffic, fx = await self.fresh(375)
            await self.login(page); await self.search(page, party); await self.select(page, ids)
            traffic.loss = 'unreadable'
            await page.get_by_test_id('booking-submit').click()
            await expect(page.get_by_test_id('booking-uncertain')).to_be_visible()
            check(await page.get_by_test_id('booking-error').count() == 0 and await page.get_by_test_id('confirmation').count() == 0,
                  'unreadable success falsely confirmed/refused')
            await page.get_by_test_id('booking-submit').click()
            await expect(page.get_by_test_id('confirmation-reference')).to_have_text(traffic.last_committed['reference'])
            check(traffic.bookings[0] == traffic.bookings[1], 'unreadable retry identity changed')
            await context.close()
            context, page, traffic, fx = await self.fresh()
            await self.login(page); await self.search(page, party); await self.select(page, ids)
            gate = traffic.gate(lambda r: urlsplit(r.url).path == '/reservations' and r.method == 'POST')
            await page.get_by_test_id('booking-submit').click()
            await asyncio.wait_for(gate['started'].wait(), 10)
            await page.get_by_test_id('booking-party-size').fill(str(party - 1))
            gate['release'].set(); await asyncio.wait_for(gate['finished'].wait(), 10)
            check(await page.get_by_test_id('confirmation').count() == 0, 'old intent callback restored confirmation')
            await self.select(page, ids, '20:00')
            await page.get_by_test_id('booking-party-size').fill(str(party - 1))
            await page.get_by_test_id('booking-submit').click()
            await expect(page.get_by_test_id('confirmation')).to_be_visible()
            check(traffic.bookings[-1]['key'] != traffic.bookings[0]['key'], 'changed input reused old request identity')
            token = traffic.bookings[-1]['authorization'].removeprefix('Bearer ')
            check(len(await self.call(self.api.reservations, token)) == 2, 'changed intent effect count incorrect')
            await context.close()

    async def lookup_detail_and_cancel_races(self):
        for variant in ('reference', 'detail', 'cancel'):
            context, page, traffic, fx = await self.fresh()
            await self.login(page); await self.search(page, 6); await self.select(page, ('a', 'z'))
            await page.get_by_test_id('booking-submit').click()
            await expect(page.get_by_test_id('confirmation')).to_be_visible()
            token = traffic.bookings[-1]['authorization'].removeprefix('Bearer ')
            rows = await self.call(self.api.reservations, token); first = rows[0]
            second = await self.call(self.api.book, token, api_checks.request(('m', 'q'), 6), 'second')
            foreign_token = await self.call(self.api.login, 'bob')
            foreign = await self.call(self.api.book, foreign_token, api_checks.request(('m',), 1, at='20:00'), 'foreign')
            await page.locator('a[data-nav][href="/lookup"]').first.click()
            field = page.get_by_test_id('lookup-reference-input')
            if variant == 'cancel':
                await field.fill(first['reference']); await page.get_by_test_id('lookup-submit').click()
                await expect(page.get_by_test_id('reservation-status')).to_have_text('confirmed')
                gate = traffic.gate(lambda r: urlsplit(r.url).path.endswith('/cancel'))
                await page.get_by_test_id('reservation-cancel-button').click()
            else:
                path = '/restaurants/r' if variant == 'detail' else '/reservations/' + first['reference']
                gate = traffic.gate(lambda r: urlsplit(r.url).path == path)
                await field.fill(first['reference']); await page.get_by_test_id('lookup-submit').click()
            await asyncio.wait_for(gate['started'].wait(), 10)
            await field.fill(second['reference']); await page.get_by_test_id('lookup-submit').click()
            await expect(page.get_by_test_id('reservation-tables')).to_contain_text('Chef’s nook')
            gate['release'].set(); await asyncio.wait_for(gate['finished'].wait(), 10)
            await expect(page.get_by_test_id('reservation-status')).to_have_text('confirmed')
            await expect(page.get_by_test_id('reservation-tables')).to_contain_text('Chef’s nook')
            await field.fill(foreign['reference']); await page.get_by_test_id('lookup-submit').click()
            await expect(page.get_by_test_id('reservation-error')).to_be_visible()
            check(await page.get_by_test_id('reservation-detail').count() == 0, 'foreign lookup leaked/stale detail')
            await context.close()

    async def desktop_long_labels_and_no_seats(self):
        for width in (375, 1280):
            fx = oracle.fixture()
            fx['restaurants'][0]['name'] = 'The Lantern Courtyard and Conservatory Dining Room'
            for table in fx['restaurants'][0]['tables']:
                table['label'] += ' beside the old olive tree and garden windows'
            context, page, traffic, _ = await self.fresh(width, fx=fx)
            await self.login(page); await self.search(page, 11); await self.grid(page, fx, 11)
            check(await page.get_by_test_id('no-slots').count() == 0, 'no seats misrepresented as no times')
            await self.visual(page, 'no-seats-' + str(width))
            await self.search(page, 6); await self.grid(page, fx, 6); await self.select(page, ('a', 'z'))
            cell = page.get_by_test_id('slot-a+z-18:00')
            await cell.focus(); await page.keyboard.press('Enter')
            await expect(page.get_by_test_id('booking-form')).to_be_visible()
            await self.visual(page, 'long-label-selected-' + str(width))
            await page.get_by_test_id('booking-submit').click()
            await expect(page.get_by_test_id('confirmation')).to_be_visible()
            await self.visual(page, 'long-label-confirmed-' + str(width))
            await page.get_by_test_id('booking-form').scroll_into_view_if_needed()
            await page.screenshot(path=str(self.out / ('long-label-confirmed-viewport-' + str(width) + '.png')),
                                  full_page=False)
            check(not traffic.blocked_hosts, 'external runtime assets requested')
            await context.close()

    async def run(self, selected=None):
        names = ['crossed_detail_closed_and_error', 'conflict_refresh_and_frozen_search_intent',
                 'unreadable_and_changed_pending_intent', 'lookup_detail_and_cancel_races', 'desktop_long_labels_and_no_seats']
        for name in selected or names:
            check(name in names, 'unknown browser protocol')
            started = time.monotonic()
            try:
                await getattr(self, name)()
                check(not self.runtime_errors, 'unhandled browser runtime error')
                result = {'case': name, 'status': 'PASS'}
            except (prior.CheckFailure, AssertionError) as error:
                result = {'case': name, 'status': 'FAIL', 'classification': 'INCONCLUSIVE', 'detail': type(error).__name__}
                result['trace'] = [{'file': Path(x.filename).name, 'line': x.lineno, 'function': x.name}
                                   for x in traceback.extract_tb(error.__traceback__)]
                for index, context in enumerate(self.browser.contexts):
                    for page in context.pages:
                        await self.screenshot(page, 'investigate-' + name + '-' + str(index))
            except Exception as error:
                result = {'case': name, 'status': 'ERROR', 'classification': 'INCONCLUSIVE', 'detail': type(error).__name__}
                result['trace'] = [{'file': Path(x.filename).name, 'line': x.lineno, 'function': x.name}
                                   for x in traceback.extract_tb(error.__traceback__)]
                for index, context in enumerate(self.browser.contexts):
                    for page in context.pages:
                        await self.screenshot(page, 'investigate-' + name + '-' + str(index))
            finally:
                for traffic in self.traffics:
                    if traffic.delayed:
                        traffic.delayed['release'].set()
                        if traffic.delayed['started'].is_set():
                            try: await asyncio.wait_for(traffic.delayed['finished'].wait(), 2)
                            except TimeoutError: pass
                for context in list(self.browser.contexts): await context.close()
            result['seconds'] = round(time.monotonic() - started, 3)
            self.results.append(result); print(json.dumps(result), flush=True)
        return {'campaign': 'independent-stage-2-explicit-protocols', 'cases': self.results,
                'all_passed': all(x['status'] == 'PASS' for x in self.results), 'runtime_errors': self.runtime_errors,
                'visual_metrics': self.visual_metrics, 'visual_review_required': True}


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['http'])
    parser.add_argument('--released', action='store_true'); parser.add_argument('--revision', required=True)
    for name in ('source', 'destination', 'third', 'legacy', 'control', 'out'):
        parser.add_argument('--' + name)
    parser.add_argument('--cases', nargs='+')
    args = parser.parse_args()
    if not args.released or not re.fullmatch('[0-9a-f]{40}', args.revision):
        parser.error('Conductor integrated exact FULL SHA required')
    out = Path(args.out); out.mkdir(parents=True, exist_ok=True)
    apis = APIExtensions(args.source, args.destination, args.third, args.legacy, args.control)
    reports = []
    for name in ('pair_selector_precedence_and_receipts', 'pair_amendment_dst_and_cutoff', 'pair_exact_sum_snapshot_transfer'):
        if args.cases and name not in args.cases: continue
        started = time.monotonic()
        try:
            await asyncio.to_thread(getattr(apis, name)); result = {'case': name, 'status': 'PASS'}
        except Exception as error:
            result = {'case': name, 'status': 'ERROR', 'classification': 'INCONCLUSIVE', 'detail': type(error).__name__}
        result['seconds'] = round(time.monotonic() - started, 3)
        reports.append(result); print(json.dumps(result), flush=True)
    browser_checks.Traffic = ExtendedTraffic
    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        selected_browser = [x for x in args.cases if not x.startswith('pair_')] if args.cases else None
        report = (await BrowserExtensions(browser, args.source, args.destination, args.legacy, out, args.control).run(selected_browser)
                  if selected_browser != [] else {'cases': [], 'visual_metrics': [], 'runtime_errors': []})
        await browser.close()
    report['cases'] = reports + report['cases']
    report['all_passed'] = all(x['status'] == 'PASS' for x in report['cases'])
    report['production_revision'] = args.revision
    timings = apis.api.timings + apis.dest.timings
    report['api_requests'] = len(timings)
    report['max_regular_request_seconds'] = max((v for p, v in timings if not p.startswith('/_test/')), default=0)
    report['max_control_request_seconds'] = max((v for p, v in timings if p.startswith('/_test/')), default=0)
    (out / 'extension-summary.json').write_text(json.dumps(report, indent=2) + '\n')
    raise SystemExit(0 if report['all_passed'] else 1)


if __name__ == '__main__':
    asyncio.run(main())
