#!/usr/bin/env python3
"""Cumulative independent API campaign. HTTP mode requires explicit full-SHA release."""
import argparse
import copy
import datetime as dt
from decimal import Decimal
import json
from pathlib import Path
import re
import threading
import time
from itertools import permutations
from concurrent.futures import ThreadPoolExecutor
import urllib.parse

import stage1_campaign as prior
import oracle

check = prior.check
DAY = prior.DAY
OriginalAPI = prior.API


class API(OriginalAPI):
    def book(self, token, value=None, key='book', status=201, code=None):
        result = self.expect(status, 'POST', '/reservations', value or prior.body(), token, key, code)
        if status in (200, 201):
            check(re.fullmatch('[A-Z0-9]{6,12}', result.get('reference', '')) is not None, 'reference format')
            check(isinstance(result.get('reservation_id'), str) and len(result['reservation_id']) <= 64, 'reservation ID')
            if status == 201:
                oracle.current_shape(result)
            for name in ('starts_at', 'ends_at', 'created_at'):
                prior.instant_seconds(result[name])
        return result

    def reservations(self, token):
        rows = self.expect(200, 'GET', '/reservations', token=token)['reservations']
        oracle.audit(rows)
        return rows

    def slots(self, day=DAY, party=2, restaurant='r'):
        q = urllib.parse.urlencode({'restaurant_id': restaurant, 'date': day, 'party_size': party})
        return self.expect(200, 'GET', '/availability?' + q)['slots']


class InheritedAPI(API):
    """Apply unchanged Stage 1 assertions to the legacy slot projection.

    Stage 2 available_options is checked fully by new option-oracle cases below.
    Only the expressly added field is projected away for old exact slot assertions.
    """
    def request(self, method, path, *args, **kwargs):
        status, value = super().request(method, path, *args, **kwargs)
        if status == 200 and path.startswith('/availability?'):
            value = copy.deepcopy(value)
            for slot in value['slots']:
                check(isinstance(slot.get('available_options'), list), 'Stage 2 option field absent')
                del slot['available_options']
        return status, value


def request(ids=('a', 'z'), party=6, at='18:00', day=DAY, restaurant='r'):
    return {'restaurant_id': restaurant, 'table_ids': list(ids), 'starts_at_local': day + 'T' + at, 'party_size': party}


class Campaign:
    def __init__(self, source, destination, third=None, legacy=None, control=None):
        self.api, self.dest = API(source), API(destination)
        self.third = API(third) if third else None
        self.legacy = OriginalAPI(legacy) if legacy else None
        self.control = Path(control) if control else None
        self.results = []

    def fresh(self, fx=None):
        self.fx = fx or oracle.fixture()
        self.api.reset(self.fx)
        self.token = self.api.login()
        return self.api, self.token

    def pause(self, name):
        check(self.control is not None, 'source-unavailability control is required')
        (self.control / ('pause-' + name)).write_text('ready\n')
        deadline = time.monotonic() + 30
        while not (self.control / (name + '-unavailable')).exists():
            if time.monotonic() >= deadline:
                raise OSError('source unavailable handshake failed')
            time.sleep(.1)

    def pair_model_and_seeds(self):
        fx = oracle.fixture()
        fx['reservations'] = [dict(request(), id='seed-pair', reference='SEEDP1', user_id='ada'),
                              dict(prior.body('m'), id='seed-single', reference='SEEDS1', user_id='ada', status='cancelled')]
        a, token = self.fresh(fx)
        rows = a.reservations(token)
        check({r['reservation_id']: r['status'] for r in rows} == {'seed-pair': 'confirmed', 'seed-single': 'cancelled'}, 'seed status/default')
        detail = a.expect(200, 'GET', '/restaurants/r')
        check(detail['combinable'] == fx['restaurants'][0]['combinable'], 'pair config/order changed')
        check(a.slots(party=1) == oracle.slots(fx, DAY, 1, rows), 'seed member occupancy')
        other = copy.deepcopy(fx['restaurants'][0]); other['id'] = 'other'; other['name'] = 'Other courtyard'
        fx['restaurants'].append(other)
        a, token = self.fresh(fx)
        check(a.slots(party=1, restaurant='other') == oracle.slots(fx, DAY, 1, a.reservations(token), 'other'), 'restaurant namespace')
        for config in (None, []):
            legacy = prior.fixture()
            if config is not None:
                legacy['restaurants'][0]['combinable'] = config
            a, _ = self.fresh(legacy)
            check(a.slots() == oracle.slots(legacy, DAY, 2), 'legacy omitted/empty pair config')

    def pair_create_validation(self):
        good = (prior.body('z'), request(('z',), 4), request(), request(('z', 'a'), 6))
        for index, value in enumerate(good):
            a, token = self.fresh()
            row = a.book(token, value, 'good')
            check(set(oracle.members(row)) == set(value.get('table_ids', [value.get('table_id')])), 'create selected wrong members')
        faults = [(request(('a', 'm'), 7), 422, 'combination_not_allowed'),
                  (request(('z', 'a', 'm'), 2), 422, 'combination_not_allowed'),
                  (request(('z', 'z'), 2), 422, 'validation_failed'),
                  ({**request(), 'table_id': 'z'}, 422, 'validation_failed'),
                  (request((), 2), 422, 'validation_failed'),
                  (request(('missing',), 1), 404, 'not_found'),
                  (request(party=7), 422, 'party_exceeds_capacity'),
                  ({**request(), 'table_ids': 'a'}, 400, 'malformed_request'),
                  ({**request(), 'table_ids': [True]}, 400, 'malformed_request'),
                  ({**request(), 'table_ids': [2]}, 400, 'malformed_request')]
        for value, status, code in faults:
            a, token = self.fresh()
            a.book(token, value, 'reusable', status, code)
            check(a.reservations(token) == [], 'rejected selection leaked record')
            check(a.slots(party=1) == oracle.slots(self.fx, DAY, 1), 'rejected selection leaked occupancy')
            a.book(token, request(), 'reusable')

    def pair_options_oracle(self):
        for step, duration in ((30, 90), (17, 43), (45, 120)):
            fx = oracle.fixture(opens='18:10', closes='23:10', slot=step, duration=duration)
            a, token = self.fresh(fx)
            for party in range(1, 12):
                check(a.slots(party=party) == oracle.slots(fx, DAY, party), 'option enumeration/capacity/order')
            chosen = oracle.slots(fx, DAY, 6)[1]['starts_at_local']
            row = a.book(token, {**request(), 'starts_at_local': chosen})
            for party in (1, 3, 6, 10, 11):
                check(a.slots(party=party) == oracle.slots(fx, DAY, party, [row]), 'any-member overlap/options')
            a.expect(200, 'POST', '/reservations/' + row['reference'] + '/cancel', token=token)
            check(a.slots() == oracle.slots(fx, DAY, 2), 'pair cancellation releases both')

    def pair_receipt_array_identity(self):
        a, token = self.fresh()
        value = {**request(), 'ignored': Decimal('1e309')}
        original = a.book(token, value, 'pair-receipt')
        equivalent = dict(reversed(list(value.items()))); equivalent['ignored'] = Decimal('10e308')
        check(a.book(token, equivalent, 'pair-receipt', 200) == original, 'object/numeric equivalent replay')
        for changed in ({**value, 'table_ids': ['z', 'a']}, {**value, 'table_ids': ['z', 'z']},
                        {**value, 'ignored': Decimal('1e310')}, {**value, 'party_size': False}):
            a.book(token, changed, 'pair-receipt', 409, 'idempotency_key_reuse')
        a.expect(200, 'POST', '/reservations/' + original['reference'] + '/cancel', token=token)
        check(a.book(token, value, 'pair-receipt', 200) == original, 'historical pair response changed')
        check(a.reservations(token)[0]['status'] == 'cancelled', 'pair replay resurrected state')
        a.book(token, request(('z', 'a')), 'new-reversed')

    def pair_patch_replacement_rollback(self):
        a, token = self.fresh()
        row = a.book(token, prior.body('z'), 'single')
        path = '/reservations/' + row['reference']
        paired = a.expect(200, 'PATCH', path, {'table_ids': ['a', 'z'], 'party_size': 6}, token)
        oracle.current_shape(paired)
        single = a.expect(200, 'PATCH', path, {'table_id': 'm'}, token)
        check(single['table_ids'] == ['m'] and single['table_id'] == 'm', 'legacy selector failed to replace pair')
        check((single['reservation_id'], single['reference'], single['created_at']) ==
              (row['reservation_id'], row['reference'], row['created_at']), 'amendment changed identity/time')
        paired = a.expect(200, 'PATCH', path, {'table_ids': ['m', 'q'], 'party_size': 8}, token)
        check(a.expect(200, 'PATCH', path, {}, token) == paired, 'pair no-op changed fields')
        before = a.reservations(token)
        for change, code in (({'table_ids': ['a', 'm']}, 'combination_not_allowed'),
                             ({'table_ids': ['a', 'z']}, 'party_exceeds_capacity'),
                             ({'table_ids': ['m', 'm']}, 'validation_failed')):
            a.expect(422, 'PATCH', path, change, token, code=code)
            check(a.reservations(token) == before, 'failed pair amendment changed records')
            check(a.slots(party=1) == oracle.slots(self.fx, DAY, 1, before), 'failed pair amendment changed occupancy')
        a.expect(200, 'POST', path + '/cancel', token=token)
        check(a.slots(party=1) == oracle.slots(self.fx, DAY, 1), 'cancel retained pair member')

    def pair_batch_final_state(self):
        a, token = self.fresh()
        one = a.book(token, request(), 'one')
        two = a.book(token, request(('m', 'q'), 8), 'two')
        move = {'moves': [{'reference': one['reference'], 'table_ids': ['m', 'q']},
                          {'reference': two['reference'], 'table_ids': ['a', 'z'], 'party_size': 6}]}
        response = a.expect(201, 'POST', '/reservation-moves', move, token, 'swap')
        check([r['reference'] for r in response['reservations']] == [one['reference'], two['reference']], 'batch input order')
        before = a.reservations(token)
        invalid = {'moves': [{'reference': one['reference'], 'table_ids': ['z', 'm']}, {'reference': two['reference']}]}
        a.expect(409, 'POST', '/reservation-moves', invalid, token, 'failed', 'table_unavailable')
        check(a.reservations(token) == before, 'failed batch partially committed')
        a.expect(201, 'POST', '/reservation-moves', {'moves': [{'reference': one['reference']}]}, token, 'failed')
        check(a.reservations(token) == before, 'no-op batch changed full values')
        # Later non-occupancy input wins over an earlier final-member conflict.
        invalid['moves'][1]['table_ids'] = ['m', 'm']
        a.expect(422, 'POST', '/reservation-moves', invalid, token, 'priority', 'validation_failed')
        check(a.reservations(token) == before, 'priority failure mutated batch')
        a.expect(200, 'POST', '/reservations/' + one['reference'] + '/cancel', token=token)
        check(a.expect(200, 'POST', '/reservation-moves', move, token, 'swap') == response, 'batch historical receipt')
        check(a.reservations(token)[0]['status'] in ('confirmed', 'cancelled'), 'state audit missing')

    def pair_dst(self):
        transitions = [('Europe/Berlin', '2026-03-29', '02:00'), ('Europe/Berlin', '2026-10-25', None),
                       ('America/New_York', '2026-03-08', '02:00'), ('America/New_York', '2026-11-01', None)]
        for zone, day, gap in transitions:
            fx = oracle.fixture(zone=zone, opens='00:00', closes='05:00'); fx['restaurants'][0]['cancellation_cutoff_minutes'] = 0
            a, token = self.fresh(fx)
            check(a.slots(day, 6) == oracle.slots(fx, day, 6), 'pair DST slot oracle')
            if gap:
                a.book(token, request(day=day, at=gap), 'gap', 422, 'invalid_local_time')
            local = '02:00' if zone == 'Europe/Berlin' and not gap else '01:00'
            row = a.book(token, request(day=day, at=local), 'dst')
            check(prior.instant_seconds(row['ends_at']) - prior.instant_seconds(row['starts_at']) == 5400, 'pair absolute duration')
            check(row['starts_at'] == prior.resolve(day + 'T' + local, zone).isoformat(), 'pair first occurrence offset')
            check(a.slots(day, 1) == oracle.slots(fx, day, 1, [row]), 'pair DST member occupancy')

    def parallel(self, functions):
        barrier = threading.Barrier(len(functions))
        def call(fn):
            barrier.wait(timeout=10)
            return fn()
        with ThreadPoolExecutor(max_workers=len(functions)) as pool:
            return list(pool.map(call, functions))

    def pair_concurrency_50(self):
        a, token = self.fresh()
        replies = self.parallel([lambda: a.request('POST', '/reservations', request(), token, 'identical') for _ in range(50)])
        check(sum(status == 201 for status, _ in replies) == 1 and sum(status == 200 for status, _ in replies) == 49,
              'concurrent identical pair receipt counts')
        check(all(value == replies[0][1] for _, value in replies), 'concurrent pair bodies differ')
        check(len(a.reservations(token)) == 1, 'duplicate pair effect')
        a, token = self.fresh()
        choices = [('a', 'z'), ('z',), ('a',), ('z', 'm'), ('m', 'q')]
        values = [request(choices[i % len(choices)], party=1) for i in range(50)]
        replies = self.parallel([lambda i=i: a.request('POST', '/reservations', values[i], token, 'contend-' + str(i)) for i in range(50)])
        check(all(s == 201 or (s == 409 and v['error']['code'] == 'table_unavailable') for s, v in replies), 'member contention status')
        rows = a.reservations(token)
        check(len(rows) == sum(s == 201 for s, _ in replies), 'record/response effect count')
        winners = [set(oracle.members(row)) for row in rows]
        for i, (status, _) in enumerate(replies):
            if status == 409:
                check(any(set(values[i]['table_ids']) & winner for winner in winners), 'rejection lacks serial blocking winner')
        check(a.slots(party=1) == oracle.slots(self.fx, DAY, 1, rows), 'concurrent option state')

    def pair_numeric_capacity(self):
        self.numeric_observations = []
        for vector in oracle.feasible_capacity_vectors():
            fx = oracle.fixture(zone='UTC')
            fx['restaurants'][0]['tables'][0]['capacity'] = vector['left']
            fx['restaurants'][0]['tables'][1]['capacity'] = vector['right']
            a = self.api
            start = len(a.timings)
            a, token = self.fresh(fx)
            exact = vector['sum']
            for threshold in (exact - 1, exact, exact + 1):
                check(a.slots(party=threshold) == oracle.slots(fx, DAY, threshold),
                      'exact capacity threshold/order mismatch')
            row = a.book(token, request(party=exact), 'giant-pair')
            check(row['party_size'] == exact, 'pair party numeric loss')
            check(a.book(token, request(party=Decimal(str(exact))), 'giant-pair', 200) == row,
                  'exact numeric-equivalent pair receipt changed')
            check(a.slots(party=exact) == oracle.slots(fx, DAY, exact, [row]),
                  'giant pair capacity option loss')
            a.book(token, request(party=exact + 1, at='20:00'), 'capacity', 422, 'party_exceeds_capacity')
            a.book(token, request(party=exact, at='20:00'), 'capacity')
            timings = a.timings[start:]
            self.numeric_observations.append({
                'input_capacity_exponents': [str(vector['left']), str(vector['right'])],
                'exact_sum_decimal_digits': vector['exact_sum_decimal_digits'],
                'threshold_deltas_checked': [-1, 0, 1], 'requests': len(timings),
                'max_regular_request_seconds': max((v for p, v in timings if not p.startswith('/_test/')), default=0),
                'max_control_request_seconds': max((v for p, v in timings if p.startswith('/_test/')), default=0)})

    def pair_reads_and_atomic_snapshots(self):
        a, token = self.fresh()
        one = a.book(token, request(), 'one')
        two = a.book(token, request(('m', 'q'), 6), 'two')
        before = a.reservations(token)
        swap = {'moves': [{'reference': one['reference'], 'table_ids': ['m', 'q']},
                          {'reference': two['reference'], 'table_ids': ['a', 'z']}]}
        responses = self.parallel([lambda: a.request('POST', '/reservation-moves', swap, token, 'atomic-swap')]
                                  + [lambda: a.request('GET', '/_test/export') for _ in range(20)])
        check(responses[0][0] == 201 and all(s == 200 for s, _ in responses[1:]), 'snapshot race response codes')
        original_response = responses[0][1]
        after = a.reservations(token)
        for _, snapshot in responses[1:]:
            self.dest.expect(204, 'POST', '/_test/import', snapshot)
            rows = self.dest.reservations(token)
            check(rows in (before, after), 'snapshot contains partial pair/batch state')
            status, receipt = self.dest.request('POST', '/reservation-moves', swap, token, 'atomic-swap')
            check(status == (201 if rows == before else 200), 'snapshot tore records and receipt')
            check(receipt == original_response, 'snapshot original batch response changed')
        a, token = self.fresh()
        one = a.book(token, request(), 'one'); two = a.book(token, request(('m', 'q'), 6), 'two')
        refs = [one['reference'], two['reference']]
        def transaction(i):
            sets = [['m', 'q'], ['a', 'z']] if i % 2 else [['a', 'z'], ['m', 'q']]
            moves = {'moves': [{'reference': ref, 'table_ids': ids} for ref, ids in zip(refs, sets)]}
            return a.request('POST', '/reservation-moves', moves, token, 'toggle-' + str(i))
        replies = self.parallel([lambda i=i: transaction(i) for i in range(25)]
                                + [lambda: a.request('GET', '/reservations', token=token) for _ in range(25)])
        check(all(s == 201 for s, _ in replies[:25]), 'legal concurrent swap rejected')
        for status, value in replies[25:]:
            check(status == 200, 'read during batch rejected')
            rows = value['reservations']; oracle.audit(rows)
            check({r['reference'] for r in rows} == set(refs), 'read lost reservation')
            check({frozenset(oracle.members(r)) for r in rows} == {frozenset(['a', 'z']), frozenset(['m', 'q'])},
                  'read exposed transient member state')

    def pair_patch_create_serial_oracle(self):
        # Three operations permit exhaustive independent serial enumeration (six orders).
        possible = set()
        for order in permutations(range(3)):
            state = {'original': frozenset(['a', 'z'])}; statuses = [None] * 3
            for index in order:
                target = frozenset(['m', 'q'] if index == 0 else ['z'] if index == 1 else ['m'])
                touched = 'original' if index == 0 else 'z' if index == 1 else 'm'
                blocked = any(name != touched and ids & target for name, ids in state.items())
                statuses[index] = 409 if blocked else 200 if index == 0 else 201
                if not blocked:
                    state[touched] = target
            possible.add((tuple(statuses), tuple(sorted((k, tuple(sorted(v))) for k, v in state.items()))))
        for _ in range(4):
            a, token = self.fresh()
            original = a.book(token, request(), 'original')
            replies = self.parallel([lambda: a.request('PATCH', '/reservations/' + original['reference'], {'table_ids': ['m', 'q']}, token),
                                     lambda: a.request('POST', '/reservations', request(('z',), 1), token, 'z'),
                                     lambda: a.request('POST', '/reservations', request(('m',), 1), token, 'm')])
            rows = a.reservations(token)
            normalized = []
            for row in rows:
                name = 'original' if row['reference'] == original['reference'] else oracle.members(row)[0]
                normalized.append((name, tuple(sorted(oracle.members(row)))))
            observed = (tuple(s for s, _ in replies), tuple(sorted(normalized)))
            check(observed in possible, 'responses/final state lack any valid serial order')

    def stage1_upgrade_receipts(self):
        check(self.legacy is not None, 'accepted Stage 1 source required')
        old = self.legacy
        old.reset(prior.fixture())
        first_token, second_token = old.login(), old.login()
        body = {**prior.body(), 'ignored': Decimal('1e309')}
        original = old.book(first_token, body, 'old-create')
        moves = {'moves': [{'reference': original['reference'], 'table_id': 'm'}]}
        original_batch = old.expect(201, 'POST', '/reservation-moves', moves, first_token, 'old-batch')
        old.expect(200, 'POST', '/reservations/' + original['reference'] + '/cancel', token=first_token)
        old.book(first_token, prior.body('a', at='18:01'), 'old-failed', 422, 'not_on_slot_grid')
        rows = old.reservations(first_token)
        snapshot = old.expect(200, 'GET', '/_test/export')
        self.pause('legacy')
        d = self.dest
        d.reset(oracle.fixture()); displaced = d.login()
        for _ in range(2):
            d.expect(204, 'POST', '/_test/import', snapshot)
            expected = [oracle.migrate_record_expectation(r) for r in rows]
            check(d.reservations(first_token) == expected and d.reservations(second_token) == expected, 'current record upgrade extension')
            check(d.reservations(d.login()) == expected, 'upgraded hashed login')
            check(d.book(first_token, body, 'old-create', 200) == original, 'legacy receipt JSON changed')
            check(d.expect(200, 'POST', '/reservation-moves', moves, first_token, 'old-batch') == original_batch, 'old batch JSON changed')
            d.expect(401, 'GET', '/reservations', token=displaced, code='unauthenticated')
            d.book(first_token, prior.body('a'), 'old-failed')
        chain = d.expect(200, 'GET', '/_test/export')
        third = self.third or d
        third.expect(204, 'POST', '/_test/import', chain)
        check(third.book(first_token, body, 'old-create', 200) == original, 'chained legacy receipt changed')

    def pair_snapshot_receipts(self):
        a, token = self.fresh()
        another = a.login()
        value = {**request(), 'ignored': Decimal('1e-1000')}
        original = a.book(token, value, 'pair-create')
        moves = {'moves': [{'reference': original['reference'], 'table_ids': ['m', 'q'], 'party_size': 8}]}
        original_batch = a.expect(201, 'POST', '/reservation-moves', moves, token, 'pair-batch')
        a.expect(200, 'POST', '/reservations/' + original['reference'] + '/cancel', token=token)
        before = a.reservations(token)
        snapshot = a.expect(200, 'GET', '/_test/export')
        a.book(token, request(), 'later')
        self.pause('source')
        d = self.dest
        d.reset(oracle.fixture()); displaced = d.login()
        for _ in range(2):
            d.expect(204, 'POST', '/_test/import', snapshot)
            check(d.reservations(token) == before and d.reservations(another) == before, 'pair snapshot changed state/session')
            check(d.book(token, value, 'pair-create', 200) == original, 'pair original receipt changed')
            check(d.expect(200, 'POST', '/reservation-moves', moves, token, 'pair-batch') == original_batch, 'batch original receipt changed')
            d.expect(401, 'GET', '/reservations', token=displaced, code='unauthenticated')
            check(d.slots(party=1) == oracle.slots(self.fx, DAY, 1, before), 'pair config/order import')
        for invalid in ({**snapshot, 'state': None}, {**snapshot, 'track': 'wrong'}):
            d.expect(422, 'POST', '/_test/import', invalid, code='validation_failed')
            check(d.reservations(token) == before, 'invalid pair import mutated state')
        third = self.third or d
        third.expect(204, 'POST', '/_test/import', d.expect(200, 'GET', '/_test/export'))
        check(third.book(token, value, 'pair-create', 200) == original, 'pair A->B->C receipt')

    def run(self, selected=None):
        names = ['pair_model_and_seeds', 'pair_create_validation', 'pair_options_oracle', 'pair_receipt_array_identity',
                 'pair_patch_replacement_rollback', 'pair_batch_final_state', 'pair_dst', 'pair_concurrency_50',
                 'pair_numeric_capacity', 'pair_reads_and_atomic_snapshots', 'pair_patch_create_serial_oracle',
                 'stage1_upgrade_receipts', 'pair_snapshot_receipts']
        for name in selected or names:
            check(name in names, 'unknown Stage 2 case')
            started = time.monotonic()
            try:
                getattr(self, name)()
                result = {'case': name, 'status': 'PASS'}
            except prior.CheckFailure as exc:
                result = {'case': name, 'status': 'FAIL', 'classification': 'PRODUCT DEFECT', 'detail': str(exc)}
            except (OSError, TimeoutError) as exc:
                result = {'case': name, 'status': 'ERROR', 'classification': 'INCONCLUSIVE', 'detail': type(exc).__name__}
            except Exception as exc:
                result = {'case': name, 'status': 'ERROR', 'classification': 'VERIFIER DEFECT', 'detail': type(exc).__name__}
            result['seconds'] = round(time.monotonic() - started, 3)
            if name == 'pair_numeric_capacity':
                result['observed_numeric_bounds'] = getattr(self, 'numeric_observations', [])
            self.results.append(result)
            print(json.dumps(result), flush=True)
        timings = sum((a.timings for a in (self.api, self.dest, self.third, self.legacy) if a is not None), [])
        return {'campaign': 'independent-stage-2-pairs', 'cases': self.results, 'requests': len(timings),
                'all_passed': all(x['status'] == 'PASS' for x in self.results),
                'max_regular_request_seconds': max((v for p, v in timings if not p.startswith('/_test/')), default=0),
                'max_control_request_seconds': max((v for p, v in timings if p.startswith('/_test/')), default=0)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['calibrate', 'http', 'inherited'])
    parser.add_argument('--revision'); parser.add_argument('--released', action='store_true')
    parser.add_argument('--source'); parser.add_argument('--destination'); parser.add_argument('--third')
    parser.add_argument('--legacy'); parser.add_argument('--control'); parser.add_argument('--out')
    parser.add_argument('--cases', nargs='+')
    args = parser.parse_args()
    if args.mode == 'calibrate':
        print(json.dumps(oracle.calibrate()))
        return
    if not args.released or not re.fullmatch('[0-9a-f]{40}', args.revision or ''):
        parser.error('Conductor full exact-SHA release required before any product request')
    if args.mode == 'inherited':
        prior.API = InheritedAPI
        report = prior.Campaign(args.source, args.destination, third=args.third).run(args.cases)
        report['campaign'] = 'independent-stage-2-inherited'
    else:
        report = Campaign(args.source, args.destination, args.third, args.legacy, args.control).run(args.cases)
    report['production_revision'] = args.revision
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2) + '\n')
    raise SystemExit(0 if report['all_passed'] else 1)


if __name__ == '__main__':
    main()
