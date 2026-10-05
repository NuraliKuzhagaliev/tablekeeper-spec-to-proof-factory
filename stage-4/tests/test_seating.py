"""Independent exhaustive optimization oracle and interacting state regressions."""
import copy
import itertools
import random
import subprocess
import sys
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from decimal import Decimal, localcontext
from unittest.mock import patch
from pathlib import Path

from domain import APIError
from json_value import dumps, loads
from seating import solve
from service import Service
from test_service import fixture


def oracle(restaurant, records, prior, closure):
    # Deliberately independent enumeration; no production occupancy, selection,
    # numeric addition, optimizer or pruning helper is used.
    def intersect(a, b):
        return datetime.fromisoformat(a[0]) < datetime.fromisoformat(b[1]) and datetime.fromisoformat(b[0]) < datetime.fromisoformat(a[1])
    considered = sorted([r for r in records if r['restaurant_id'] == restaurant['id'] and r['status'] == 'confirmed'
                         and intersect((r['starts_at'], r['ends_at']), (closure['from'], closure['to']))], key=lambda r: r['reference'])
    fixed = [r for r in records if r['restaurant_id'] == restaurant['id'] and r['status'] == 'confirmed' and r not in considered]
    options = [[t['id']] for t in restaurant['tables']] + restaurant['combinable']
    winner = None
    with localcontext() as context:
        context.prec = 2000
        for vector in itertools.product(range(len(options)), repeat=len(considered)):
            waste, moved, legal = Decimal(0), 0, True
            for index, (record, rank) in enumerate(zip(considered, vector)):
                tables = options[rank]
                def exact(value):
                    return Decimal(value.token if hasattr(value, 'token') else str(value))
                capacity = sum((exact(record['accepted_terms']['capacities'][table]) for table in tables), Decimal(0))
                interval = record['starts_at'], record['ends_at']
                if capacity < exact(record['party_size']):
                    legal = False; break
                if any(c['table_id'] in tables and intersect(interval, (c['from'], c['to'])) for c in [*prior, closure]):
                    legal = False; break
                if any(set(tables) & set(other['table_ids']) and intersect(interval, (other['starts_at'], other['ends_at'])) for other in fixed):
                    legal = False; break
                if any(set(tables) & set(options[vector[j]]) and intersect(interval, (other['starts_at'], other['ends_at']))
                       for j, other in enumerate(considered[:index])):
                    legal = False; break
                moved += set(tables) != set(record['table_ids'])
                waste += capacity - exact(record['party_size'])
            if legal and (winner is None or (moved, waste, vector) < winner):
                winner = moved, waste, vector
    if winner is None:
        return None
    return {'assignments': [{'reference': r['reference'], 'table_ids': options[rank],
                            'changed': set(options[rank]) != set(r['table_ids'])} for r, rank in zip(considered, winner[2])],
            'moved_count': winner[0], 'unused_seats': winner[1]}


class SeatingTests(unittest.TestCase):
    def setUp(self):
        self.s = Service()
        data = fixture('UTC')
        data['restaurants'][0].update(manager_user_ids=['alice'], combinable=[['t2', 't1']])
        self.call('POST', '/_test/reset', data)
        self.token = self.call('POST', '/auth/login', {'email': 'alice@example.com', 'password': 'password123'})[1]['token']
        self.other = self.call('POST', '/auth/login', {'email': 'bob@example.com', 'password': 'password456'})[1]['token']

    def call(self, method, path, body=None, key=None, token=None, query=None):
        headers = {} if token is False else {'Authorization': 'Bearer ' + (token or getattr(self, 'token', ''))}
        if key is not None:
            headers['Idempotency-Key'] = key
        return self.s.request(method, path, query or {}, body or {}, headers)

    def error(self, code, callback):
        with self.assertRaises(APIError) as result:
            callback()
        self.assertEqual(result.exception.code, code)

    def create(self, key='booking', table='t1', start='2032-06-03T18:00', count=4, token=None):
        return self.call('POST', '/reservations', {'restaurant_id': 'r', 'table_id': table, 'starts_at_local': start, 'party_size': count}, key, token)[1]

    def preview(self, key='preview', table='t1', start='2032-06-03T18:00:00+00:00', end='2032-06-03T19:00:00+00:00'):
        return self.call('POST', '/restaurants/r/replans', {'table_id': table, 'from': start, 'to': end}, key)[1]

    def apply(self, plan, key='apply'):
        return self.call('POST', '/restaurants/r/replans/' + plan['plan_id'] + '/apply', {}, key)

    def snapshot(self):
        return self.call('GET', '/_test/export')[1]

    def series(self, count=3):
        anchor = self.create()
        return self.call('POST', '/series', {'anchor_reference': anchor['reference'], 'count': count, 'interval_weeks': 1}, 'adopt')[1]

    def amend(self, agreement, body, key='amend'):
        return self.call('POST', '/series/' + agreement['series_id'] + '/amend', body, key)

    def test_optimizer_matches_independent_exhaustive_oracle(self):
        rng = random.Random(419)
        for case in range(50):
            restaurant = {'id': 'r', 'tables': [{'id': 't' + str(i)} for i in range(4)],
                          'combinable': [['t1', 't0'], ['t2', 't1'], ['t3', 't0']]}
            records = []
            for index in range(rng.randint(1, 4)):
                capacity = {table['id']: rng.randint(2, 9) for table in restaurant['tables']}
                records.append({'restaurant_id': 'r', 'reference': 'REF' + str(9 - index), 'status': 'confirmed',
                                'table_ids': ['t' + str(index)], 'party_size': rng.randint(1, capacity['t' + str(index)]),
                                'accepted_terms': {'capacities': capacity},
                                'starts_at': '2032-06-03T18:00:00+00:00', 'ends_at': f'2032-06-03T{19 if index >= 2 else rng.choice((19,20,21))}:00:00+00:00'})
            records.append({'restaurant_id': 'r', 'reference': 'FIXED', 'status': 'confirmed', 'table_ids': ['t3'],
                            'starts_at': '2032-06-03T20:00:00+00:00', 'ends_at': '2032-06-03T22:00:00+00:00'})
            closure = {'table_id': 't' + str(rng.randrange(4)), 'from': '2032-06-03T18:30:00+00:00', 'to': '2032-06-03T19:00:00+00:00'}
            prior = [{'table_id': 't2', 'from': '2032-06-03T20:00:00+00:00', 'to': '2032-06-03T21:00:00+00:00'}]
            expected = oracle(restaurant, records, prior, closure)
            with self.subTest(case=case):
                if expected is None:
                    self.error('no_feasible_plan', lambda: solve(restaurant, records, prior, closure))
                else:
                    self.assertEqual(solve(restaurant, records, prior, closure), expected)

    def test_preview_read_only_and_manager_application_preserves_other_owner(self):
        record = self.create(token=self.other)
        before = copy.deepcopy(self.s.state)
        plan = self.preview()
        self.assertEqual(plan['assignments'], [{'reference': record['reference'], 'table_ids': ['t2'], 'changed': True}])
        for key in ('reservations', 'histories', 'series', 'closures', 'restaurant_revisions'):
            self.assertEqual(self.s.state[key], before[key])
        applied = self.apply(plan)[1]
        moved = applied['reservations'][0]
        self.assertEqual(moved, {**record, 'table_id': 't2', 'table_ids': ['t2'], 'revision': 2})
        self.error('not_found', lambda: self.call('GET', '/reservations/' + record['reference']))
        history = self.call('GET', '/reservations/' + record['reference'] + '/history', token=self.other)[1]
        event = history['entries'][-1]
        self.assertEqual(event['event'], 'reassigned')
        self.assertEqual(event['plan_id'], plan['plan_id'])
        self.assertEqual(event['changes'], [{'field': 'table_ids', 'from': ['t1'], 'to': ['t2']}])
        snapshot = self.snapshot()
        self.call('POST', '/_test/import', snapshot)
        self.assertEqual(self.snapshot(), snapshot)
        self.assertEqual(self.apply(plan), (200, applied))

    def test_manager_permissions_interval_validation_and_failed_keys(self):
        body = {'table_id': 't1', 'from': '2032-06-03T18:00:00Z', 'to': '2032-06-03T19:00:00Z'}
        for token, code in ((False, 'unauthenticated'), (self.other, 'forbidden')):
            self.error(code, lambda: self.call('POST', '/restaurants/r/replans', body, 'p', token))
        self.error('missing_idempotency_key', lambda: self.call('POST', '/restaurants/r/replans', body))
        for invalid in ({'from': '2032-06-03T18:00:00'}, {'to': body['from']}, {'table_id': 'missing'}):
            code = 'not_found' if 'table_id' in invalid else 'validation_failed'
            before = self.snapshot()
            self.error(code, lambda: self.call('POST', '/restaurants/r/replans', {**body, **invalid}, 'reusable'))
            self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.call('POST', '/restaurants/r/replans', body, 'reusable')[0], 201)

    def test_half_open_closure_and_submicrosecond_interval_precision(self):
        plan = self.preview(start='2032-06-03T17:59:59.99999999Z', end='2032-06-03T18:00:00Z')
        self.apply(plan)
        self.create()
        # Distinct legitimate fractional instants must not truncate to equality.
        tiny = self.preview('tiny', start='2032-06-03T19:30:00.00000001Z', end='2032-06-03T19:30:00.00000002Z')
        self.assertEqual(tiny['assignments'], [])
        self.apply(tiny, 'tiny-apply')
        self.error('table_unavailable', lambda: self.create('second', start='2032-06-03T19:30'))
        self.call('POST', '/_test/import', self.snapshot())

    def test_receipt_then_already_applied_then_stale_and_local_revision(self):
        self.create()
        old = self.preview()
        self.create('later', start='2032-06-03T20:00')
        before = self.snapshot()
        self.error('stale_plan', lambda: self.apply(old))
        self.assertEqual(self.snapshot(), before)
        current = self.preview('current')
        applied = self.apply(current)[1]
        self.error('plan_already_applied', lambda: self.apply(current, 'different'))
        self.assertEqual(self.apply(current), (200, applied))
        route = '/restaurants/r/replans/' + current['plan_id'] + '/apply'
        self.error('idempotency_key_reuse', lambda: self.call('POST', route, {'ignored': False}, 'apply'))
        self.assertEqual(self.call('POST', '/restaurants/r/replans', {'table_id': 't1', 'from': '2032-06-03T18:00:00+00:00', 'to': '2032-06-03T19:00:00+00:00'}, 'current'), (200, current))

    def test_zero_moved_application_counts_once_and_closes_every_member_option(self):
        plan = self.preview()
        self.assertEqual(plan['moved_count'], 0)
        self.assertEqual(self.s.state['restaurant_revisions']['r'], 0)
        self.apply(plan)
        self.assertEqual(self.s.state['restaurant_revisions']['r'], 1)
        slot = next(s for s in self.call('GET', '/availability', query={'restaurant_id': 'r', 'date': '2032-06-03', 'party_size': '4', 'explain': 'true'})[1]['slots'] if s['starts_at_local'].endswith('18:00'))
        self.assertEqual(slot['available_table_ids'], ['t2'])
        self.assertEqual(slot['available_options'], [{'table_ids': ['t2'], 'capacity': 6}])
        self.assertFalse(slot['explain'][0]['rules'][1]['holds'])
        self.error('table_unavailable', lambda: self.create())
        self.error('table_unavailable', lambda: self.call('POST', '/reservations', {'restaurant_id': 'r', 'table_ids': ['t1', 't2'], 'starts_at_local': '2032-06-03T18:00', 'party_size': 6}, 'pair'))

    def test_operator_bypasses_cutoff_and_preserves_series_exception_flags(self):
        agreement = self.series()
        sibling = agreement['occurrences'][1]['reference']
        self.call('PATCH', '/reservations/' + sibling, {'party_size': 3})
        before = self.call('GET', '/series/' + agreement['series_id'])[1]
        plan = self.preview(end='2032-06-17T20:00:00Z')
        with patch('service.datetime') as clock:
            clock.now.return_value = datetime(2033, 1, 1, tzinfo=timezone.utc)
            self.apply(plan)
        after = self.call('GET', '/series/' + agreement['series_id'])[1]
        self.assertEqual(after['revision'], before['revision'] + 1)
        self.assertEqual([x['exception'] for x in after['occurrences']], [False, True, False])
        self.assertTrue(all(x['reservation']['table_ids'] == ['t2'] for x in after['occurrences']))
        self.call('POST', '/_test/import', self.snapshot())

    def test_collective_series_changes_current_repaired_tables_and_excludes_exceptions_cancelled(self):
        agreement = self.series(4)
        sid = agreement['series_id']
        refs = [x['reference'] for x in agreement['occurrences']]
        self.call('PATCH', '/reservations/' + refs[1], {'party_size': 3})
        self.call('POST', '/reservations/' + refs[2] + '/cancel')
        plan = self.preview(end='2032-06-24T20:00:00Z')
        self.apply(plan)
        current = self.call('GET', '/series/' + sid)[1]
        response = self.amend(current, {'expected_revision': current['revision'], 'from_index': 0, 'local_time': '20:00'})[1]
        self.assertEqual(response['revision'], current['revision'] + 1)
        for index in (0, 3):
            self.assertEqual(response['occurrences'][index]['reservation']['starts_at_local'], agreement['occurrences'][index]['reservation']['starts_at_local'][:10] + 'T20:00')
            self.assertEqual(response['occurrences'][index]['reservation']['table_ids'], ['t2'])
            self.assertFalse(response['occurrences'][index]['exception'])
        for index in (1, 2):
            self.assertEqual(response['occurrences'][index], current['occurrences'][index])
        self.call('POST', '/_test/import', self.snapshot())

    def test_series_noop_and_empty_require_cas_but_not_expired_cutoff(self):
        agreement = self.series(2)
        body = {'expected_revision': 1, 'from_index': 0, 'local_time': '18:00'}
        before = copy.deepcopy(self.s.state)
        with patch('service.datetime') as clock:
            clock.now.return_value = datetime(2033, 1, 1, tzinfo=timezone.utc)
            self.assertEqual(self.amend(agreement, body)[1], agreement)
            self.error('stale_revision', lambda: self.amend(agreement, {**body, 'expected_revision': 99}, 'stale'))
            self.error('cutoff_passed', lambda: self.amend(agreement, {**body, 'local_time': '20:00'}, 'real'))
        for key in ('reservations', 'histories', 'series', 'restaurant_revisions'):
            self.assertEqual(self.s.state[key], before[key])
        for item in agreement['occurrences']:
            self.call('POST', '/reservations/' + item['reference'] + '/cancel')
        current = self.call('GET', '/series/' + agreement['series_id'])[1]
        self.assertEqual(self.amend(current, {'expected_revision': current['revision'], 'from_index': 0, 'local_time': '20:00'}, 'empty')[1], current)
        self.call('POST', '/_test/import', self.snapshot())

    def test_series_nonoccupancy_before_final_conflict_and_complete_rollback(self):
        agreement = self.series()
        self.create('block', table='t1', start='2032-06-03T20:00')
        policy = {'effective_from': '2032-06-10', 'slot_minutes': 30, 'reservation_duration_minutes': 90,
                  'cancellation_cutoff_minutes': 120, 'opening_hours': [{'weekday': 'thu', 'opens': '00:00', 'closes': '23:30'}],
                  'capacities': {'t1': 1, 't2': 6}}
        self.call('POST', '/restaurants/r/policies', policy, 'policy')
        before = self.snapshot()
        body = {'expected_revision': 1, 'from_index': 0, 'local_time': '20:00'}
        self.error('party_exceeds_capacity', lambda: self.amend(agreement, body))
        self.assertEqual(self.snapshot(), before)
        self.error('stale_revision', lambda: self.amend(agreement, {**body, 'expected_revision': 9}))
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.amend(agreement, {**body, 'local_time': '18:00'})[0], 201)

    def test_parallel_application_and_series_cas_exactly_once(self):
        agreement = self.series()
        plan = self.preview()
        barrier = threading.Barrier(50)
        def apply(_):
            barrier.wait()
            return self.apply(plan)
        with ThreadPoolExecutor(max_workers=50) as pool:
            responses = list(pool.map(apply, range(50)))
        self.assertEqual(sum(status == 201 for status, _ in responses), 1)
        self.assertTrue(all(body == responses[0][1] for _, body in responses))
        current = self.call('GET', '/series/' + agreement['series_id'])[1]
        barrier = threading.Barrier(50)
        def amend(index):
            barrier.wait()
            try:
                return self.amend(current, {'expected_revision': current['revision'], 'from_index': 0, 'local_time': '20:00'}, 'amend-' + str(index))[0]
            except APIError as error:
                return error.code
        with ThreadPoolExecutor(max_workers=50) as pool:
            results = list(pool.map(amend, range(50)))
        self.assertEqual(results.count(201), 1)
        self.assertEqual(results.count('stale_revision'), 49)
        self.call('POST', '/_test/import', self.snapshot())

    def test_corrupt_plan_closure_schedule_and_history_import_rollback(self):
        agreement = self.series()
        plan = self.preview()
        self.apply(plan)
        empty = self.preview('empty-preview', table='t2', start='2034-06-03T18:00:00Z', end='2034-06-03T19:00:00Z')
        self.apply(empty, 'empty-apply')
        snapshot = self.snapshot()
        state = loads(snapshot['state']['payload'])
        mutations = []
        bad = copy.deepcopy(state); bad['plans'][plan['plan_id']]['response']['unused_seats'] += 1; mutations.append(bad)
        bad = copy.deepcopy(state); bad['closures']['r'][0]['to'] = bad['closures']['r'][0]['from']; mutations.append(bad)
        bad = copy.deepcopy(state); bad['series'][agreement['series_id']]['occurrences'][0]['scheduled_date'] = '2032-07-01'; mutations.append(bad)
        bad = copy.deepcopy(state); bad['histories'][agreement['occurrences'][0]['reference']]['entries'][-1]['plan_id'] = 'missing'; mutations.append(bad)
        bad = copy.deepcopy(state); bad['histories'][agreement['occurrences'][0]['reference']]['entries'][-1]['plan_id'] = empty['plan_id']; mutations.append(bad)
        for invalid in mutations:
            self.error('validation_failed', lambda: self.call('POST', '/_test/import', {**snapshot, 'state': {'encoding': 'tablekeeper-json-v1', 'payload': dumps(invalid)}}))
            self.assertEqual(self.snapshot(), snapshot)

    def test_actual_populated_stage3_import_preserves_schedules_receipts_and_known_counters(self):
        # A separate interpreter loads the actual frozen Stage3 modules, not the
        # current implementation. Credentials/exports remain only in test memory.
        source = Path(__file__).resolve().parents[2] / 'stage-3'
        script = r'''
from service import Service
from json_value import dumps
s=Service()
def call(method,path,body=None,key=None,token=None):
    h={'Authorization':'Bearer '+token} if token else {}
    if key: h['Idempotency-Key']=key
    return s.request(method,path,{},body or {},h)
fixture={'users':[{'id':'alice','email':'a@local','password':'password123','display_name':'Alice'},
                  {'id':'bob','email':'b@local','password':'password456','display_name':'Bob'}],
 'restaurants':[{'id':'r','name':'Restaurant','timezone':'UTC','slot_minutes':30,'reservation_duration_minutes':90,
 'cancellation_cutoff_minutes':120,'opening_hours':[{'weekday':w,'opens':'00:00','closes':'23:30'} for w in ('mon','tue','wed','thu','fri','sat','sun')],
 'tables':[{'id':'t1','label':'One','capacity':4},{'id':'t2','label':'Two','capacity':6}],
 'combinable':[['t2','t1']],'manager_user_ids':['alice']}],'reservations':[]}
call('POST','/_test/reset',fixture)
a=call('POST','/auth/login',{'email':'a@local','password':'password123'})[1]['token']
a2=call('POST','/auth/login',{'email':'a@local','password':'password123'})[1]['token']
b=call('POST','/auth/login',{'email':'b@local','password':'password456'})[1]['token']
create={'restaurant_id':'r','table_id':'t1','starts_at_local':'2032-06-03T18:00','party_size':4,'ignored':1}
original=call('POST','/reservations',create,'create',a)[1]
adopt={'anchor_reference':original['reference'],'count':4,'interval_weeks':1}
agreement=call('POST','/series',adopt,'adopt',a)[1]
call('PATCH','/reservations/'+original['reference'],{'starts_at_local':'2032-06-04T18:00','table_id':'t2'},token=a)
batch={'moves':[{'reference':agreement['occurrences'][1]['reference'],'party_size':3}]}
moved=call('POST','/reservation-moves',batch,'batch',a)[1]
call('POST','/reservations/'+agreement['occurrences'][2]['reference']+'/cancel',token=a)
policy={'effective_from':'2032-06-10','slot_minutes':30,'reservation_duration_minutes':60,'cancellation_cutoff_minutes':30,
 'opening_hours':fixture['restaurants'][0]['opening_hours'],'capacities':{'t1':4,'t2':6}}
published=call('POST','/restaurants/r/policies',policy,'policy',a)[1]
print(dumps({'snapshot':call('GET','/_test/export')[1],'a':a,'a2':a2,'b':b,'create':create,'original':original,
             'adopt':adopt,'agreement':agreement,'batch':batch,'moved':moved,'policy':policy,'published':published,
             'current':call('GET','/series/'+agreement['series_id'],token=a)[1],'counter':s.state['restaurant_revisions']['r']}))
'''
        imported = loads(subprocess.check_output([sys.executable, '-B', '-c', script], cwd=source, text=True))
        self.call('POST', '/_test/import', imported['snapshot'])
        self.token = imported['a']
        self.other = imported['b']
        self.assertEqual(self.s.state['restaurant_revisions']['r'], imported['counter'])
        current = self.call('GET', '/series/' + imported['agreement']['series_id'], token=imported['a2'])[1]
        self.assertEqual(current, imported['current'])
        self.assertEqual(self.call('POST', '/reservations', imported['create'], 'create'), (200, imported['original']))
        self.assertEqual(self.call('POST', '/reservation-moves', imported['batch'], 'batch'), (200, imported['moved']))
        self.assertEqual(self.call('POST', '/series', imported['adopt'], 'adopt'), (200, imported['agreement']))
        self.assertEqual(self.call('POST', '/restaurants/r/policies', imported['policy'], 'policy'), (200, imported['published']))
        plan = self.preview(start='2032-06-24T18:00:00Z', end='2032-06-24T19:00:00Z')
        self.apply(plan)
        repaired = self.call('GET', '/series/' + current['series_id'])[1]
        amended = self.amend(repaired, {'expected_revision': repaired['revision'], 'from_index': 0, 'local_time': '20:00'})[1]
        last = amended['occurrences'][3]['reservation']
        self.assertEqual(last['starts_at_local'], '2032-06-24T20:00')
        self.assertEqual(last['table_ids'], ['t2'])
        self.assertEqual(last['accepted_terms']['policy_version'], 1)
        self.assertEqual(last['ends_at'], '2032-06-24T21:00:00+00:00')
        self.assertEqual(amended['occurrences'][:3], repaired['occurrences'][:3])
        snapshot = self.snapshot()
        self.call('POST', '/_test/import', snapshot)
        self.assertEqual(self.snapshot(), snapshot)
        self.assertEqual(self.call('POST', '/series', imported['adopt'], 'adopt'), (200, imported['agreement']))

    def test_preview_contenders_and_snapshot_observe_complete_apply_generation(self):
        self.create()
        body = {'table_id': 't1', 'from': '2032-06-03T18:00:00Z', 'to': '2032-06-03T19:00:00Z'}
        barrier = threading.Barrier(50)
        def preview(_):
            barrier.wait()
            return self.call('POST', '/restaurants/r/replans', body, 'same-preview')
        with ThreadPoolExecutor(max_workers=50) as pool:
            results = list(pool.map(preview, range(50)))
        self.assertEqual(sum(status == 201 for status, _ in results), 1)
        self.assertTrue(all(body == results[0][1] for _, body in results))
        plan = results[0][1]
        barrier = threading.Barrier(50)
        def snapshot(index):
            barrier.wait()
            if index == 0:
                self.apply(plan)
            state = loads(self.snapshot()['state']['payload'])
            moved = state['plans'][plan['plan_id']]['applied']
            record = next(iter(state['reservations'].values()))
            self.assertEqual(record['table_ids'], ['t2'] if moved else ['t1'])
            self.assertEqual(record['revision'], 2 if moved else 1)
            self.assertEqual(state['restaurant_revisions']['r'], 2 if moved else 1)
            self.assertEqual(len(state['closures']['r']), 1 if moved else 0)
            self.assertEqual(len(state['receipts']), 3 if moved else 2)
            return state
        with ThreadPoolExecutor(max_workers=50) as pool:
            list(pool.map(snapshot, range(50)))
        self.call('POST', '/_test/import', self.snapshot())

    def test_every_revision_family_and_other_restaurant_isolation(self):
        data = fixture('UTC')
        one = data['restaurants'][0]
        one['manager_user_ids'] = ['alice']
        second = copy.deepcopy(one); second['id'] = 'other'
        data['restaurants'].append(second)
        self.call('POST', '/_test/reset', data)
        self.token = self.call('POST', '/auth/login', {'email': 'alice@example.com', 'password': 'password123'})[1]['token']
        record = self.create()
        plan = self.preview()
        self.call('POST', '/reservations', {'restaurant_id': 'other', 'table_id': 't1', 'starts_at_local': '2032-06-03T18:00', 'party_size': 4}, 'other')
        self.apply(plan)
        self.assertEqual(self.s.state['restaurant_revisions'], {'r': 2, 'other': 1})
        route = '/reservations/' + record['reference']
        self.call('PATCH', route, {'table_id': 't2'})
        self.assertEqual(self.s.state['restaurant_revisions']['r'], 2)
        self.call('PATCH', route, {'party_size': 3})
        self.assertEqual(self.s.state['restaurant_revisions']['r'], 3)
        self.call('POST', route + '/cancel')
        self.call('POST', route + '/cancel')
        self.assertEqual(self.s.state['restaurant_revisions']['r'], 4)
        policy = {'effective_from': '2032-06-10', 'slot_minutes': 30, 'reservation_duration_minutes': 90,
                  'cancellation_cutoff_minutes': 120, 'opening_hours': one['opening_hours'], 'capacities': {'t1': 4, 't2': 6}}
        self.call('POST', '/restaurants/r/policies', policy, 'policy')
        self.call('POST', '/restaurants/r/policies', policy, 'policy')
        self.assertEqual(self.s.state['restaurant_revisions']['r'], 5)

    def test_series_control_types_privacy_closure_conflict_and_retry_identity(self):
        agreement = self.series()
        body = {'expected_revision': 1, 'from_index': 0, 'local_time': '20:00'}
        route = '/series/' + agreement['series_id'] + '/amend'
        self.error('unauthenticated', lambda: self.call('POST', route, body, 'amend', False))
        self.error('not_found', lambda: self.call('POST', route, body, 'amend', self.other))
        for field, value in [('expected_revision', True), ('expected_revision', 0), ('from_index', False),
                             ('from_index', 3), ('local_time', '20:00:00'), ('local_time', None)]:
            before = self.snapshot()
            self.error('validation_failed', lambda: self.amend(agreement, {**body, field: value}))
            self.assertEqual(self.snapshot(), before)
        plan = self.preview(start='2032-06-03T20:00:00Z', end='2032-06-03T21:00:00Z')
        self.apply(plan)
        self.error('table_unavailable', lambda: self.amend(agreement, body))
        response = self.amend(agreement, {**body, 'local_time': '22:00'})[1]
        self.error('idempotency_key_reuse', lambda: self.amend(agreement, body))
        self.assertEqual(self.amend(agreement, {**body, 'local_time': '22:00'}), (200, response))
        self.call('POST', '/_test/import', self.snapshot())

    def test_maximum_supported_shape_and_exact_large_capacity_objective(self):
        restaurant = {'id': 'r', 'tables': [{'id': 't' + str(i)} for i in range(6)],
                      'combinable': [['t0', 't1'], ['t2', 't1'], ['t3', 't4'], ['t5', 't0']]}
        records = [{'reference': 'REF' + str(i), 'restaurant_id': 'r', 'status': 'confirmed', 'table_ids': ['t' + str(i)],
                    'party_size': 2, 'accepted_terms': {'capacities': {'t' + str(j): 2 for j in range(6)}},
                    'starts_at': f'2032-06-03T{12+i}:00:00+00:00', 'ends_at': f'2032-06-03T{13+i}:00:00+00:00'} for i in range(6)]
        closure = {'table_id': 't5', 'from': '2032-06-03T12:00:00Z', 'to': '2032-06-03T18:00:00Z'}
        result = solve(restaurant, records, [], closure)
        self.assertEqual(result['moved_count'], 1)
        self.assertEqual(result['unused_seats'], 0)
        self.assertEqual(result['assignments'][-1]['table_ids'], ['t0'])
        records[0]['accepted_terms']['capacities'] = {'t0': 2, 't1': loads('1e309'), 't2': 10**309 + 1, 't3': 10**310, 't4': 10**311, 't5': 10**312}
        closure['table_id'] = 't0'
        expected = oracle(restaurant, records[:1], [], closure)
        actual = solve(restaurant, records[:1], [], closure)
        self.assertEqual(actual['assignments'], expected['assignments'])
        self.assertEqual(actual['moved_count'], expected['moved_count'])
        self.assertEqual(Decimal(actual['unused_seats'].token), expected['unused_seats'])
        # Zero additions must not expand a mathematically compact giant value.
        from json_value import add_numbers
        self.assertEqual(dumps(add_numbers(0, loads('1e1000000000'))), '1e1000000000')

    def test_planning_limits_rollback_at_each_stated_boundary(self):
        for kind in ('tables', 'pairs', 'bookings'):
            data = fixture('UTC')
            restaurant = data['restaurants'][0]
            restaurant['manager_user_ids'] = ['alice']
            restaurant['reservation_duration_minutes'] = 60
            restaurant['tables'] = [{'id': 't' + str(i), 'label': str(i), 'capacity': 2} for i in range(7 if kind == 'tables' else 6)]
            restaurant['combinable'] = [['t' + str(i), 't' + str(i+1)] for i in range(5 if kind == 'pairs' else 4)]
            if kind == 'bookings':
                data['reservations'] = [{'id': 'seed' + str(i), 'reference': 'SEED00' + str(i), 'user_id': 'alice', 'restaurant_id': 'r',
                                         'table_id': 't0', 'starts_at_local': f'2032-06-03T0{i}:00', 'party_size': 2} for i in range(7)]
            self.call('POST', '/_test/reset', data)
            self.token = self.call('POST', '/auth/login', {'email': 'alice@example.com', 'password': 'password123'})[1]['token']
            before = self.snapshot()
            with self.subTest(kind=kind):
                self.error('planning_limit', lambda: self.preview(start='2032-06-03T00:00:00Z', end='2032-06-03T07:00:00Z'))
                self.assertEqual(self.snapshot(), before)
