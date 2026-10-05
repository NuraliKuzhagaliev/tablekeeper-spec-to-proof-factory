"""Interaction regressions for retained terms, immutable history and agreements."""
import copy
import subprocess
import sys
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from unittest.mock import patch

from domain import APIError, overlaps, read_timestamp
from json_value import dumps, loads
from service import Service
from test_service import fixture


def policy_fixture(zone='UTC', date='2032-06-03'):
    data = fixture(zone, date)
    data['restaurants'][0].update(manager_user_ids=['alice'], combinable=[['t2', 't1']])
    return data


class PolicySeriesTests(unittest.TestCase):
    def setUp(self):
        self.s = Service()
        self.call('POST', '/_test/reset', policy_fixture())
        self.token = self.call('POST', '/auth/login', {'email': 'alice@example.com', 'password': 'password123'})[1]['token']
        self.other = self.call('POST', '/auth/login', {'email': 'bob@example.com', 'password': 'password456'})[1]['token']

    def call(self, method, path, body=None, key=None, token=None, query=None):
        headers = {'Authorization': 'Bearer ' + (token or getattr(self, 'token', ''))} if token is not False else {}
        if key is not None:
            headers['Idempotency-Key'] = key
        return self.s.request(method, path, query or {}, body or {}, headers)

    def error(self, callback, code, status=None):
        with self.assertRaises(APIError) as error:
            callback()
        self.assertEqual(error.exception.code, code)
        if status:
            self.assertEqual(error.exception.status, status)

    def create(self, key='create', start='2032-06-03T18:00', selection=None, count=4, token=None):
        body = {'restaurant_id': 'r', 'starts_at_local': start, 'party_size': count, **(selection or {'table_id': 't1'})}
        return self.call('POST', '/reservations', body, key, token)[1]

    def policy(self, effective='2032-05-01', duration=120, cutoff=60, capacity=4, hours=None):
        return {'effective_from': effective, 'slot_minutes': 30, 'reservation_duration_minutes': duration,
                'cancellation_cutoff_minutes': cutoff, 'opening_hours': hours if hours is not None else
                [{'weekday': 'thu', 'opens': '00:00', 'closes': '23:30'}], 'capacities': {'t1': capacity, 't2': 6}}

    def publish(self, body, key='policy'):
        return self.call('POST', '/restaurants/r/policies', body, key)[1]

    def history(self, record):
        return self.call('GET', '/reservations/' + record['reference'] + '/history')[1]

    def snapshot(self):
        return self.call('GET', '/_test/export')[1]

    def test_policy_permissions_validation_and_receipt_precedence(self):
        self.error(lambda: self.call('POST', '/restaurants/r/policies', self.policy(), 'p', token=False), 'unauthenticated', 401)
        self.error(lambda: self.call('POST', '/restaurants/r/policies', self.policy(), 'p', token=self.other), 'forbidden', 403)
        self.error(lambda: self.call('POST', '/restaurants/unknown/policies', self.policy(), 'p'), 'not_found', 404)
        before = self.snapshot()
        for key, value in [('slot_minutes', True), ('slot_minutes', 1441), ('reservation_duration_minutes', 0),
                           ('cancellation_cutoff_minutes', 10081), ('effective_from', '2032-02-30'),
                           ('capacities', {'t1': 4}), ('capacities', {'t1': 101, 't2': 6}),
                           ('opening_hours', [{'weekday': 'thu', 'opens': '18:00', 'closes': '17:00'}])]:
            self.error(lambda: self.publish({**self.policy(), key: value}, 'failed'), 'validation_failed', 422)
            self.assertEqual(self.snapshot(), before)
        original = self.publish(self.policy(), 'failed')
        self.assertEqual(original['policy_version'], 1)
        self.assertEqual(self.call('POST', '/restaurants/r/policies', self.policy(), 'failed'), (200, original))
        self.error(lambda: self.publish({'capacities': False}, 'failed'), 'idempotency_key_reuse', 409)
        self.assertEqual(self.call('GET', '/restaurants/r/policies', token=False)[1]['policies'], [original])

    def test_effective_dates_and_version_ties_not_publication_order(self):
        detail = self.call('GET', '/restaurants/r')[1]
        self.publish(self.policy('2032-05-01', capacity=5), 'one')
        self.publish(self.policy('2032-06-01', capacity=2), 'two')
        self.publish(self.policy('2032-05-20', capacity=3), 'three')
        result = self.create(count=2)
        self.assertEqual(result['accepted_terms']['policy_version'], 2)
        self.assertEqual(result['accepted_terms']['capacities']['t1'], 2)
        self.assertNotIn('effective_from', result['accepted_terms'])
        self.publish(self.policy('2032-06-01', duration=30, capacity=4), 'four')
        fresh = self.create('fresh', start='2032-06-03T20:00')
        self.assertEqual(fresh['accepted_terms']['policy_version'], 4)
        self.assertEqual(fresh['ends_at'], '2032-06-03T20:30:00+00:00')
        self.assertEqual(self.call('GET', '/restaurants/r')[1], detail)
        self.assertEqual(self.call('GET', '/reservations/' + result['reference'])[1], result)

    def test_noop_retains_terms_even_if_new_policy_rejects_and_real_change_adopts(self):
        original = self.create()
        route = '/reservations/' + original['reference']
        initial_history = self.history(original)
        self.publish(self.policy(duration=30, capacity=2))
        self.assertEqual(self.call('PATCH', route, {'party_size': 4.0, 'expected_revision': 1, 'ignored': True})[1], original)
        self.assertEqual(self.history(original), initial_history)
        amended = self.call('PATCH', route, {'party_size': 2, 'expected_revision': 1})[1]
        self.assertEqual(amended['revision'], 2)
        self.assertEqual(amended['accepted_terms']['policy_version'], 1)
        self.assertEqual(amended['ends_at'], '2032-06-03T18:30:00+00:00')
        self.publish(self.policy(hours=[]), 'closed')
        self.assertEqual(self.call('PATCH', route, {})[1], amended)
        before = self.snapshot()
        self.error(lambda: self.call('PATCH', route, {'party_size': 3}), 'outside_opening_hours', 422)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(initial_history['entries'][0]['accepted_terms']['policy_version'], 0)

    def test_stale_revision_precedes_cutoff_and_invalid_changes(self):
        original = self.create()
        route = '/reservations/' + original['reference']
        with patch('service.datetime') as clock:
            clock.now.return_value = datetime(2032, 6, 3, 17, 0, tzinfo=timezone.utc)
            self.error(lambda: self.call('PATCH', route, {'expected_revision': 2, 'party_size': False}), 'stale_revision', 409)
            self.error(lambda: self.call('PATCH', route, {'expected_revision': True}), 'validation_failed', 422)
            self.error(lambda: self.call('PATCH', route, {'expected_revision': 1, 'party_size': False}), 'cutoff_passed', 409)
        before = self.snapshot()
        barrier = threading.Barrier(50)
        def change(index):
            barrier.wait()
            try:
                return self.call('PATCH', route, {'expected_revision': 1, 'party_size': 2 + index % 2})[0]
            except APIError as error:
                return error.code
        with ThreadPoolExecutor(max_workers=50) as pool:
            outcomes = list(pool.map(change, range(50)))
        self.assertEqual(outcomes.count(200), 1)
        self.assertEqual(outcomes.count('stale_revision'), 49)
        self.assertEqual(len(self.history(original)['entries']), 2)

    def test_accepted_cutoff_controls_cancel_not_current_policy(self):
        self.publish(self.policy(cutoff=10), 'old')
        original = self.create()
        self.publish(self.policy(cutoff=10080), 'new')
        with patch('service.datetime') as clock:
            clock.now.return_value = datetime(2032, 6, 3, 17, 0, tzinfo=timezone.utc)
            cancelled = self.call('POST', '/reservations/' + original['reference'] + '/cancel')[1]
        self.assertEqual(cancelled['revision'], 2)
        self.assertEqual(cancelled['accepted_terms'], original['accepted_terms'])
        self.assertEqual(self.call('POST', '/reservations/' + original['reference'] + '/cancel')[1], cancelled)
        self.assertEqual([event['event'] for event in self.history(original)['entries']], ['created', 'cancelled'])

    def test_explanations_report_independent_false_rules_and_policy_version(self):
        self.create()
        query = {'restaurant_id': 'r', 'date': '2032-06-03', 'party_size': '5'}
        plain = self.call('GET', '/availability', query=query)[1]
        self.assertTrue(all('explain' not in slot for slot in plain['slots']))
        explained = self.call('GET', '/availability', query={**query, 'explain': 'true'})[1]
        slot = next(slot for slot in explained['slots'] if slot['starts_at_local'].endswith('18:00'))
        self.assertEqual(slot['explain'][0], {'table_id': 't1', 'policy_version': 0, 'available': False,
                         'rules': [{'rule': 'capacity', 'holds': False}, {'rule': 'no_overlap', 'holds': False}]})
        self.assertEqual([item['table_id'] for item in slot['explain'] if item['available']], slot['available_table_ids'])
        for value in ('false', '1', ''):
            self.error(lambda: self.call('GET', '/availability', query={**query, 'explain': value}), 'validation_failed', 422)
        self.assertEqual(self.call('GET', '/availability', query={**query, 'date': '2032-06-04', 'explain': 'true'})[1]['slots'], [])

    def test_pair_history_actual_fields_and_native_terminal_sequence(self):
        record = self.create(selection={'table_ids': ['t1', 't2']}, count=6)
        route = '/reservations/' + record['reference']
        self.assertEqual(self.history(record)['entries'][0]['changes'][0], {'field': 'table_ids', 'from': None, 'to': ['t2', 't1']})
        self.assertEqual(self.call('PATCH', route, {'table_ids': ['t1', 't2']})[1], record)
        self.call('PATCH', route, {'party_size': 5})
        self.assertEqual([change['field'] for change in self.history(record)['entries'][-1]['changes']], ['party_size'])
        self.call('PATCH', route, {'table_id': 't1', 'party_size': 3})
        self.assertEqual(self.history(record)['entries'][-1]['changes'][0], {'field': 'table_ids', 'from': ['t2', 't1'], 'to': ['t1']})
        self.call('PATCH', route, {'table_id': 't2'})
        self.assertEqual(self.history(record)['entries'][-1]['changes'][0]['field'], 'table_id')
        self.call('POST', route + '/cancel')
        history = self.history(record)
        self.assertEqual([event['seq'] for event in history['entries']], [1, 2, 3, 4, 5])
        self.assertEqual([event['revision'] for event in history['entries']], [1, 2, 3, 4, 5])
        self.assertEqual(history['entries'][-1]['changes'], [])
        for suffix in ('/history', '/decision'):
            self.error(lambda: self.call('GET', route + suffix, token=False), 'not_found', 404)
            self.error(lambda: self.call('GET', route + suffix, token=self.other), 'not_found', 404)
        self.assertEqual(self.call('GET', route + '/decision')[1]['revision'], 5)
        snapshot = self.snapshot()
        self.call('POST', '/_test/import', snapshot)
        self.assertEqual(self.snapshot(), snapshot)

    def test_series_retains_anchor_and_per_date_policy_then_permanent_exceptions(self):
        anchor = self.create(selection={'table_ids': ['t1', 't2']}, count=6)
        history = self.history(anchor)
        self.publish(self.policy('2032-06-10', duration=30, capacity=2))
        request = {'anchor_reference': anchor['reference'], 'count': 3, 'interval_weeks': 1}
        agreement = self.call('POST', '/series', request, 'series')[1]
        self.assertEqual(agreement['occurrences'][0]['reservation'], anchor)
        self.assertEqual(self.history(anchor), history)
        self.assertEqual([item['reservation']['accepted_terms']['policy_version'] for item in agreement['occurrences']], [0, 1, 1])
        sibling = agreement['occurrences'][1]['reference']
        route = '/reservations/' + sibling
        self.call('PATCH', route, {'party_size': 5})
        current = self.call('GET', '/series/' + agreement['series_id'])[1]
        self.assertEqual(current['revision'], 2)
        self.assertTrue(current['occurrences'][1]['exception'])
        self.call('PATCH', route, {'party_size': 6})
        self.call('POST', route + '/cancel')
        self.call('POST', '/reservations/' + anchor['reference'] + '/cancel')
        current = self.call('GET', '/series/' + agreement['series_id'])[1]
        self.assertEqual(current['revision'], 5)
        self.assertTrue(current['occurrences'][1]['exception'])
        self.assertFalse(current['occurrences'][0]['exception'])
        self.assertEqual(current['occurrences'][2]['reservation']['status'], 'confirmed')
        self.assertEqual(self.call('POST', '/series', request, 'series'), (200, agreement))
        for token in (False, self.other):
            self.error(lambda: self.call('GET', '/series/' + agreement['series_id'], token=token), 'not_found', 404)
        snapshot = self.snapshot()
        self.call('POST', '/_test/import', snapshot)
        self.assertEqual(self.snapshot(), snapshot)
        self.assertEqual(self.call('POST', '/series', request, 'series'), (200, agreement))

    def test_failed_adoption_first_index_conflict_precedes_later_policy_invalidity(self):
        anchor = self.create()
        blocker = self.create('blocker', start='2032-06-10T18:00')
        self.publish(self.policy('2032-06-17', capacity=1))
        request = {'anchor_reference': anchor['reference'], 'count': 3, 'interval_weeks': 1}
        before = self.snapshot()
        self.error(lambda: self.call('POST', '/series', request, 'failed'), 'table_unavailable', 409)
        self.assertEqual(self.snapshot(), before)
        self.call('POST', '/reservations/' + blocker['reference'] + '/cancel')
        before = self.snapshot()
        self.error(lambda: self.call('POST', '/series', request, 'failed'), 'party_exceeds_capacity', 422)
        self.assertEqual(self.snapshot(), before)
        request['count'] = 2
        self.assertEqual(self.call('POST', '/series', request, 'failed')[0], 201)

    def test_parallel_adoption_same_key_commits_one_agreement_and_receipt(self):
        anchor = self.create()
        request = {'anchor_reference': anchor['reference'], 'count': 3, 'interval_weeks': 1}
        barrier = threading.Barrier(50)
        def execute(_):
            barrier.wait()
            return self.call('POST', '/series', request, 'one-series')
        with ThreadPoolExecutor(max_workers=50) as pool:
            outcomes = list(pool.map(execute, range(50)))
        self.assertEqual(sum(status == 201 for status, _ in outcomes), 1)
        self.assertEqual(sum(status == 200 for status, _ in outcomes), 49)
        self.assertTrue(all(response == outcomes[0][1] for _, response in outcomes))
        self.assertEqual(len(self.s.state['series']), 1)
        self.assertEqual(len(self.s.state['reservations']), 3)
        self.assertEqual(self.s.state['restaurant_revisions']['r'], 2)
        self.error(lambda: self.call('POST', '/series', request, 'another-key'), 'already_in_series', 409)

    def test_parallel_policy_publication_versions_and_receipts(self):
        barrier = threading.Barrier(50)
        body = self.policy()
        def publish(_):
            barrier.wait()
            return self.call('POST', '/restaurants/r/policies', body, 'same-policy')
        with ThreadPoolExecutor(max_workers=50) as pool:
            responses = list(pool.map(publish, range(50)))
        self.assertEqual(sum(status == 201 for status, _ in responses), 1)
        self.assertEqual(sum(status == 200 for status, _ in responses), 49)
        self.assertTrue(all(response == responses[0][1] for _, response in responses))
        with ThreadPoolExecutor(max_workers=50) as pool:
            versions = list(pool.map(lambda index: self.publish(body, 'unique-' + str(index))['policy_version'], range(50)))
        self.assertEqual(sorted(versions), list(range(2, 52)))
        self.assertEqual([item['policy_version'] for item in self.call('GET', '/restaurants/r/policies')[1]['policies']], list(range(1, 52)))

    def test_calendar_boundary_adoption_fails_without_partial_state(self):
        data = policy_fixture(date='9999-12-31')
        self.call('POST', '/_test/reset', data)
        self.token = self.call('POST', '/auth/login', {'email': 'alice@example.com', 'password': 'password123'})[1]['token']
        anchor = self.create(start='9999-12-31T18:00')
        before = self.snapshot()
        self.error(lambda: self.call('POST', '/series', {'anchor_reference': anchor['reference'], 'count': 2, 'interval_weeks': 1}, 'overflow'), 'validation_failed', 422)
        self.assertEqual(self.snapshot(), before)

    def test_concurrent_export_observes_whole_adoption_and_history_publication(self):
        anchor = self.create()
        request = {'anchor_reference': anchor['reference'], 'count': 12, 'interval_weeks': 1}
        barrier = threading.Barrier(50)
        def execute(index):
            barrier.wait()
            if index == 0:
                self.call('POST', '/series', request, 'adopt')
            snapshot = loads(self.snapshot()['state']['payload'])
            refs = set(snapshot['reservations'])
            self.assertEqual(refs, set(snapshot['histories']))
            self.assertIn(len(refs), (1, 12))
            self.assertEqual(snapshot['restaurant_revisions']['r'], 1 if len(refs) == 1 else 2)
            self.assertEqual(len(snapshot['series']), 0 if len(refs) == 1 else 1)
            if snapshot['series']:
                agreement = next(iter(snapshot['series'].values()))
                self.assertEqual({item['reference'] for item in agreement['occurrences']}, refs)
                self.assertEqual(len(snapshot['receipts']), 2)
            return snapshot
        with ThreadPoolExecutor(max_workers=50) as pool:
            list(pool.map(execute, range(50)))

    def test_collective_changed_series_once_unchanged_series_zero_and_snapshot_rollback(self):
        anchor = self.create()
        other = self.create('other', selection={'table_id': 't2'})
        one = self.call('POST', '/series', {'anchor_reference': anchor['reference'], 'count': 3, 'interval_weeks': 1}, 'one')[1]
        two = self.call('POST', '/series', {'anchor_reference': other['reference'], 'count': 2, 'interval_weeks': 1}, 'two')[1]
        request = {'moves': [{'reference': item['reference'], 'party_size': 2} for item in one['occurrences'][:2]] +
                            [{'reference': two['occurrences'][0]['reference']}]}
        moved = self.call('POST', '/reservation-moves', request, 'batch')[1]
        self.assertEqual(self.s.state['restaurant_revisions']['r'], 5)
        self.assertEqual(self.call('GET', '/series/' + one['series_id'])[1]['revision'], 2)
        self.assertEqual(self.call('GET', '/series/' + two['series_id'])[1]['revision'], 1)
        self.assertEqual(self.call('POST', '/reservation-moves', request, 'noop')[1], moved)
        self.assertEqual(self.s.state['restaurant_revisions']['r'], 5)
        before = self.snapshot()
        bad = {'moves': [{'reference': anchor['reference'], 'table_id': 't2'},
                         {'reference': other['reference'], 'expected_revision': 999, 'party_size': False}]}
        self.error(lambda: self.call('POST', '/reservation-moves', bad, 'bad'), 'stale_revision', 409)
        self.assertEqual(self.snapshot(), before)
        self.call('POST', '/_test/import', before)
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(self.call('POST', '/reservation-moves', request, 'batch'), (200, moved))

    def test_series_calendar_dst_gap_rolls_back_and_fall_uses_first_occurrence(self):
        for zone, day, clock, offset in [('America/New_York', '2026-03-01', '02:30', None),
                                       ('Europe/Berlin', '2026-03-22', '02:30', None),
                                       ('America/New_York', '2026-10-25', '01:30', '-04:00'),
                                       ('Europe/Berlin', '2026-10-18', '02:30', '+02:00')]:
            with self.subTest(zone=zone, day=day):
                self.call('POST', '/_test/reset', policy_fixture(zone, day))
                self.token = self.call('POST', '/auth/login', {'email': 'alice@example.com', 'password': 'password123'})[1]['token']
                anchor = self.create(start=day + 'T' + clock)
                before = self.snapshot()
                with patch('service.datetime') as now:
                    now.now.return_value = datetime(2026, 2, 1, tzinfo=timezone.utc)
                    request = {'anchor_reference': anchor['reference'], 'count': 2, 'interval_weeks': 1}
                    if offset is None:
                        self.error(lambda: self.call('POST', '/series', request, 'dst'), 'invalid_local_time', 422)
                        self.assertEqual(self.snapshot(), before)
                    else:
                        result = self.call('POST', '/series', request, 'dst')[1]['occurrences'][1]['reservation']
                        self.assertTrue(result['starts_at'].endswith(offset))
                        self.assertEqual((read_timestamp(result['ends_at']) - read_timestamp(result['starts_at'])).total_seconds(), 5400)

    def test_bad_native_history_import_is_rejected_without_changes(self):
        anchor = self.create()
        self.call('PATCH', '/reservations/' + anchor['reference'], {'party_size': 2})
        before = self.snapshot()
        state = loads(before['state']['payload'])
        state['histories'][anchor['reference']]['entries'][1]['changes'][0]['from'] = 999
        corrupt = {**before, 'state': {**before['state'], 'payload': dumps(state)}}
        self.error(lambda: self.call('POST', '/_test/import', corrupt), 'validation_failed', 422)
        self.assertEqual(self.snapshot(), before)

    def test_actual_populated_stage1_and_stage2_import_adoption_and_exact_old_receipts(self):
        script = '''
import sys
from service import Service
from json_value import dumps, loads
from domain import APIError
s=Service()
data=loads(sys.stdin.read())
s.request('POST','/_test/reset',{},data,{})
token=s.request('POST','/auth/login',{}, {'email':'alice@example.com','password':'password123'},{})[1]['token']
other=s.request('POST','/auth/login',{}, {'email':'alice@example.com','password':'password123'},{})[1]['token']
body={'restaurant_id':'r','starts_at_local':'2032-06-03T18:00','party_size':4}
body['ignored']=loads('1e309')
body.update({'table_ids':['t2','t1']} if 'combinable' in data['restaurants'][0] else {'table_id':'t1'})
if 'table_id' in body:
 body['table_ids']=False  # A then-unknown field must stay in the exact old receipt.
body['expected_revision']=False
headers={'Authorization':'Bearer '+token,'Idempotency-Key':'old'}
original=s.request('POST','/reservations',{},body,headers)[1]
move={'moves':[{'reference':original['reference'],'party_size':2}]}
move['moves'][0]['expected_revision']=False
if 'table_id' in body:
 move['moves'][0]['table_ids']=False
headers['Idempotency-Key']='batch'
batch=s.request('POST','/reservation-moves',{},move,headers)[1]
bob=s.request('POST','/auth/login',{}, {'email':'bob@example.com','password':'password456'},{})[1]['token']
bob_body={'restaurant_id':'r','table_id':'t2','starts_at_local':'2032-06-03T20:00','party_size':2}
cancelled=s.request('POST','/reservations',{},bob_body,{'Authorization':'Bearer '+bob,'Idempotency-Key':'bob'})[1]
s.request('POST','/reservations/'+cancelled['reference']+'/cancel',{},{},{'Authorization':'Bearer '+bob})
headers['Idempotency-Key']='failed'
try:
 s.request('POST','/reservations',{}, {'party_size':False},headers)
except APIError:
 pass
print(dumps({'snapshot':s.request('GET','/_test/export',{},{},{})[1],'token':token,'other':other,'bob':bob,'cancelled':cancelled,'bob_body':bob_body,'body':body,'original':original,'move':move,'batch':batch}))
'''
        for stage in (1, 2):
            with self.subTest(stage=stage):
                data = fixture(zone='UTC')
                if stage == 2:
                    data['restaurants'][0]['combinable'] = [['t2', 't1']]
                result = subprocess.run([sys.executable, '-B', '-c', script], cwd=Path(__file__).resolve().parents[2] / ('stage-' + str(stage)),
                                        input=dumps(data), text=True, capture_output=True, check=True)
                source = loads(result.stdout)
                replaced_token = self.token
                self.call('POST', '/_test/import', source['snapshot'])
                self.token = source['token']
                current = self.call('GET', '/reservations/' + source['original']['reference'])[1]
                self.assertEqual(current['revision'], 1)
                self.assertEqual(current['accepted_terms']['policy_version'], 0)
                self.assertEqual(self.call('POST', '/reservations', source['body'], 'old'), (200, source['original']))
                self.assertEqual(self.call('POST', '/reservation-moves', source['move'], 'batch'), (200, source['batch']))
                legacy_history = self.history(current)
                self.assertEqual(legacy_history['entries'], [])
                self.assertEqual(legacy_history['provenance'], {'kind': 'legacy_baseline', 'known_state': current})
                cancelled = self.call('GET', '/reservations/' + source['cancelled']['reference'], token=source['bob'])[1]
                self.assertEqual(cancelled['status'], 'cancelled')
                self.assertEqual(self.call('GET', '/reservations/' + cancelled['reference'] + '/history', token=source['bob'])[1]['entries'], [])
                self.assertEqual(self.call('POST', '/reservations', source['bob_body'], 'bob', token=source['bob']), (200, source['cancelled']))
                self.error(lambda: self.call('GET', '/reservations', token=replaced_token), 'unauthenticated', 401)
                agreement = self.call('POST', '/series', {'anchor_reference': current['reference'], 'count': 2, 'interval_weeks': 1}, 'adopt')[1]
                self.assertEqual(agreement['occurrences'][0]['reservation'], current)
                self.assertEqual(self.history(current), legacy_history)
                self.call('PATCH', '/reservations/' + current['reference'], {'party_size': 1})
                self.assertEqual(self.history(current)['entries'][0]['event'], 'changed')
                self.assertEqual(self.history(current)['entries'][0]['seq'], 1)
                series_now = self.call('GET', '/series/' + agreement['series_id'])[1]
                series_changed = self.call('POST', '/series/' + agreement['series_id'] + '/amend',
                        {'expected_revision': series_now['revision'], 'from_index': 0, 'local_time': '22:00'}, 'upgrade-amend')[1]
                self.assertEqual(series_changed['occurrences'][0], series_now['occurrences'][0])
                self.assertEqual(series_changed['occurrences'][1]['reservation']['starts_at_local'], '2032-06-10T22:00')
                self.assertEqual(self.s.state['restaurant_revisions']['r'], 3)
                self.assertEqual(self.call('GET', '/restaurants/r')[1]['manager_user_ids'], [])
                self.error(lambda: self.call('POST', '/restaurants/r/replans',
                    {'table_id': 't1', 'from': '2032-06-03T18:00:00Z', 'to': '2032-06-03T19:00:00Z'}, 'not-manager'), 'forbidden', 403)
                snapshot = self.snapshot()
                self.call('POST', '/_test/import', snapshot)
                self.assertEqual(self.snapshot(), snapshot)
                self.assertEqual(self.call('POST', '/reservations', source['body'], 'old'), (200, source['original']))
                self.assertEqual(self.call('GET', '/reservations', token=source['other'])[0], 200)
                fresh = {**source['body'], 'starts_at_local': '2032-06-03T20:00'}
                if stage == 1:
                    fresh.pop('table_ids')  # First use validates today's selector contract.
                self.assertEqual(self.call('POST', '/reservations', fresh, 'failed')[0], 201)


if __name__ == '__main__':
    unittest.main()
