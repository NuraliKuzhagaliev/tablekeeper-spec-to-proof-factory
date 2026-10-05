#!/usr/bin/env python3
"""Independent cumulative Stage 3 HTTP preparation; exact-SHA gate mandatory.

Opaque exports, login material and response bodies remain in memory. Outputs contain
case names/counts/timings only. A failed assertion requires reproduction and triage;
this executable never grants acceptance by itself.
"""
import argparse
import copy
import datetime as dt
import json
from pathlib import Path
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from decimal import Decimal
import urllib.parse

import policy_oracle as model
import stage1_campaign as prior
import oracle as pair_model
import campaign as pair_campaign

check = prior.check
DAY = prior.DAY


class API(pair_campaign.API):
    def current(self, ref, token):
        value = self.expect(200, 'GET', '/reservations/' + ref, token=token)
        current_shape(value)
        return value

    def history(self, ref, token):
        value = self.expect(200, 'GET', '/reservations/' + ref + '/history', token=token)
        check(value['reference'] == ref, 'history reference mismatch')
        rows = value['entries']
        check([x['seq'] for x in rows] == list(range(1, len(rows) + 1)), 'non-contiguous history')
        instants = [prior.instant_seconds(x['at']) for x in rows]
        check(instants == sorted(instants), 'history timestamps decrease')
        check(all(isinstance(x['revision'], int) and not isinstance(x['revision'], bool)
                  and x['revision'] > 0 and isinstance(x['accepted_terms'], dict) for x in rows),
              'history revision/terms shape')
        check(not any(x['event'] == 'cancelled' for x in rows[:-1]), 'history follows cancellation')
        return rows


def current_shape(value):
    pair_model.current_shape(value)
    revision = value.get('revision')
    check(isinstance(revision, int) and not isinstance(revision, bool) and revision > 0, 'current revision')
    terms = value.get('accepted_terms')
    check(isinstance(terms, dict) and set(terms) == {'policy_version', *model.FIELDS}, 'full accepted terms shape')
    check(prior.instant_seconds(value['ends_at']) - prior.instant_seconds(value['starts_at'])
          == terms['reservation_duration_minutes'] * 60, 'accepted absolute duration')


def coordinated(workers):
    check(1 <= len(workers) <= 50, 'concurrency exceeds contract')
    barrier = threading.Barrier(len(workers))
    def run(callback):
        barrier.wait(timeout=10)
        return callback()
    with ThreadPoolExecutor(max_workers=len(workers)) as pool:
        return list(pool.map(run, workers))


class Campaign:
    def __init__(self, source, destination, third, stage1=None, stage2=None, control=None):
        self.api, self.dest, self.third = API(source), API(destination), API(third)
        self.legacy = {1: prior.API(stage1) if stage1 else None,
                       2: pair_campaign.API(stage2) if stage2 else None}
        self.control = Path(control) if control else None
        self.results = []

    def fresh(self, fx=None):
        self.fx = fx or model.fixture()
        self.r = self.fx['restaurants'][0]
        self.api.reset(self.fx)
        self.token = self.api.login()
        self.publications = []
        return self.api, self.token

    def publish(self, value=None, key=None):
        value = value or model.policy(self.r, DAY)
        response = self.api.expect(201, 'POST', '/restaurants/r/policies', value, self.token,
                                   key or 'policy-' + str(len(self.publications)))
        check(response['policy_version'] == len(self.publications) + 1, 'publication version gap')
        check({k: response[k] for k in value if k in ('effective_from', *model.FIELDS)}
              == {k: value[k] for k in value if k in ('effective_from', *model.FIELDS)}, 'policy values changed')
        self.publications.append(copy.deepcopy(response))
        return response

    def book(self, table='z', at='18:00', day=DAY, party=2, key='create', ids=None):
        body = prior.body(table, at, day, party)
        if ids is not None:
            body.pop('table_id'); body['table_ids'] = ids
        value = self.api.book(self.token, body, key)
        current_shape(value)
        check(value['revision'] == 1 and value['accepted_terms'] == model.selected(self.r, self.publications, day),
              'creation terms/revision differ from selected policy')
        return value, body

    def unchanged(self, before, history):
        check(self.api.current(before['reference'], self.token) == before, 'failed/no-op changed record')
        check(self.api.history(before['reference'], self.token) == history, 'failed/no-op changed history')

    def permissions_policy_validation(self):
        a, token = self.fresh()
        path = '/restaurants/r/policies'; value = model.policy(self.r, DAY)
        a.expect(401, 'POST', path, value, key='anonymous', code='unauthenticated')
        bob = a.login('bob')
        a.expect(403, 'POST', path, value, bob, 'nonmanager', 'forbidden')
        a.expect(404, 'POST', '/restaurants/unknown/policies', value, token, 'unknown', 'not_found')
        a.expect(400, 'POST', path, value, token, code='missing_idempotency_key')
        a.expect(422, 'POST', path, value, token, 'x' * 256, 'validation_failed')
        invalid = []
        for field in value:
            invalid.append({k: v for k, v in value.items() if k != field})
        for field, bads in [('slot_minutes', [0, 1441, True, '30', None, 1.5]),
                            ('reservation_duration_minutes', [0, 1441, False, [], 1.5]),
                            ('cancellation_cutoff_minutes', [-1, 10081, True, {}, 1.5]),
                            ('effective_from', ['2080-02-30', '2080-6-6', '', 1, None])]:
            invalid += [{**value, field: bad} for bad in bads]
        for bad in [{}, {**value['capacities'], 'extra': 2}, {**value['capacities'], 'z': 0},
                    {**value['capacities'], 'z': 101}, {**value['capacities'], 'z': True},
                    {**value['capacities'], 'z': '2'}]:
            invalid.append({**value, 'capacities': bad})
        invalid += [{**value, 'opening_hours': [value['opening_hours'][0]] * 2},
                    {**value, 'opening_hours': [{'weekday': 'xxx', 'opens': '18:00', 'closes': '23:00'}]},
                    {**value, 'opening_hours': [{'weekday': 'mon', 'opens': '23:00', 'closes': '18:00'}]}]
        for item in invalid:
            a.expect(422, 'POST', path, item, token, 'failed-key', 'validation_failed')
            check(a.expect(200, 'GET', path) == {'policies': []}, 'invalid policy allocated state')
        original = self.publish({**value, 'ignored': Decimal('1e309')}, 'failed-key')
        check(a.expect(200, 'POST', path, {**value, 'ignored': Decimal('10e308')}, token, 'failed-key') == original,
              'equivalent exact numeric policy replay')
        a.expect(409, 'POST', path, {**value, 'ignored': Decimal('1e-309')}, token,
                 'failed-key', 'idempotency_key_reuse')
        check(a.expect(200, 'GET', '/restaurants/r')['slot_minutes'] == self.r['slot_minutes'], 'policy changed original detail')
        # Default manager permission is empty, not inferred from being the fixture owner.
        fx = model.fixture(); fx['restaurants'][0].pop('manager_user_ids')
        self.fresh(fx)
        a.expect(403, 'POST', path, value, self.token, 'default-empty', 'forbidden')

    def effective_date_explanations(self):
        a, token = self.fresh()
        original, _ = self.book()
        old_history = a.history(original['reference'], token)
        for date, duration in [('2080-06-01', 120), ('2080-05-01', 60), ('2080-06-01', 30)]:
            self.publish(model.policy(self.r, date, reservation_duration_minutes=duration))
        for day in ['2080-04-30', '2080-05-01', '2080-05-31', '2080-06-01', DAY]:
            for party in [1, 3, 7, 101]:
                query = urllib.parse.urlencode({'restaurant_id': 'r', 'date': day, 'party_size': party})
                expected = model.slots(self.r, self.publications, day, party, [original])
                check(a.expect(200, 'GET', '/availability?' + query)['slots'] == expected, 'policy slot oracle')
                explained = a.expect(200, 'GET', '/availability?' + query + '&explain=true')['slots']
                check(explained == model.slots(self.r, self.publications, day, party, [original], True), 'independent explanation truth matrix')
        for value in ['', 'false', '1', 'True', 'TRUE', '0']:
            a.expect(422, 'GET', '/availability?restaurant_id=r&date=' + DAY + '&party_size=2&explain=' + value,
                     code='validation_failed')
        self.unchanged(original, old_history)
        check(a.expect(200, 'GET', '/restaurants/r/policies')['policies'] == self.publications, 'publication-order list')

    def terms_history_noops_and_pairs(self):
        a, token = self.fresh()
        before, body = self.book(ids=['z', 'a'], party=6)
        history = a.history(before['reference'], token)
        check(len(history) == 1 and history[0]['event'] == 'created'
              and history[0]['changes'] == model.changes(self.r, None, before)
              and history[0]['accepted_terms'] == before['accepted_terms'], 'pair creation history')
        restrictive = model.policy(self.r, DAY, capacities={x['id']: 1 for x in self.r['tables']},
                                   reservation_duration_minutes=180)
        self.publish(restrictive)
        path = '/reservations/' + before['reference']
        for patch in [{}, {'table_ids': ['z', 'a']}, {'party_size': 6}, {'ignored': Decimal('1e-1000')}]:
            check(a.expect(200, 'PATCH', path, patch, token) == before, 'no-op adopted newer policy')
            self.unchanged(before, history)
        a.expect(422, 'PATCH', path, {'starts_at_local': DAY + 'T18:30'}, token, code='party_exceeds_capacity')
        self.unchanged(before, history)
        changed = a.expect(200, 'PATCH', path, {'table_id': 'm', 'party_size': 1}, token)
        current_shape(changed)
        check(changed['revision'] == 2 and changed['accepted_terms'] == model.selected(self.r, self.publications, DAY), 'real terms/revision')
        next_history = a.history(before['reference'], token)
        check(next_history[:-1] == history and next_history[-1]['changes'] == model.changes(self.r, before, changed)
              and next_history[-1]['revision'] == 2 and next_history[-1]['accepted_terms'] == changed['accepted_terms'], 'immutable actual-field history')
        check(a.book(token, body, 'create', 200) == before, 'old original response changed')
        cancelled = a.expect(200, 'POST', path + '/cancel', token=token)
        check(cancelled['revision'] == 3, 'cancel revision increment')
        final = a.history(before['reference'], token)
        check(final[-1]['event'] == 'cancelled' and final[-1]['changes'] == [] and final[:-1] == next_history, 'cancel terminal history')
        check(a.expect(200, 'POST', path + '/cancel', token=token) == cancelled, 'repeat cancel changes record')
        check(a.history(before['reference'], token) == final, 'repeat cancel adds history')

    def revision_priority_and_concurrency(self):
        a, token = self.fresh()
        row, _ = self.book(); path = '/reservations/' + row['reference']
        before = a.history(row['reference'], token)
        for expected in [0, -1, True, False, '1', 1.5, None, []]:
            a.expect(422, 'PATCH', path, {'expected_revision': expected}, token, code='validation_failed')
        a.expect(409, 'PATCH', path, {'expected_revision': 2, 'party_size': 'invalid'}, token, code='stale_revision')
        self.unchanged(row, before)
        # All contenders make a real change from revision 1; identical proposed values
        # do not allow a later success because expected_revision is checked first.
        workers = [lambda: a.request('PATCH', path, {'expected_revision': 1, 'party_size': 3}, token)
                   for _ in range(50)]
        responses = coordinated(workers)
        check(sum(s == 200 for s, _ in responses) == 1, 'CAS committed more/less than one change')
        check(all(s == 200 or (s == 409 and v['error']['code'] == 'stale_revision') for s, v in responses), 'CAS error results')
        current = a.current(row['reference'], token)
        check(current['revision'] == 2 and current['party_size'] == 3 and len(a.history(row['reference'], token)) == 2, 'CAS record/history atomicity')
        for suffix in ['/history', '/decision']:
            for caller in [None, 'unknown', a.login('bob')]:
                a.expect(404, 'GET', path + suffix, token=caller, code='not_found')
        check(a.expect(200, 'GET', path + '/decision', token=token)
              == {'reference': row['reference'], 'revision': 2, 'accepted_terms': current['accepted_terms']}, 'current decision')

    def publication_concurrency_receipts(self):
        a, token = self.fresh()
        value = model.policy(self.r, DAY)
        replies = coordinated([lambda: a.request('POST', '/restaurants/r/policies', value, token, 'same-policy') for _ in range(50)])
        check(sum(s == 201 for s, _ in replies) == 1 and sum(s == 200 for s, _ in replies) == 49, 'policy retry allocation')
        check(all(v == replies[0][1] for _, v in replies), 'policy retries differ')
        check(len(a.expect(200, 'GET', '/restaurants/r/policies')['policies']) == 1, 'policy retry duplicated state')
        replies = coordinated([lambda i=i: a.request('POST', '/restaurants/r/policies', value, token, 'independent-' + str(i)) for i in range(50)])
        check(all(s == 201 for s, _ in replies) and sorted(v['policy_version'] for _, v in replies) == list(range(2, 52)), 'concurrent policy version sequence')
        a.expect(409, 'POST', '/restaurants/r/policies', {}, token, 'same-policy', 'idempotency_key_reuse')

    def series_anchor_and_exceptions(self):
        a, token = self.fresh()
        anchor, body = self.book()
        saved_history = a.history(anchor['reference'], token)
        value = {'anchor_reference': anchor['reference'], 'count': 4, 'interval_weeks': 1}
        self.publish(model.policy(self.r, '2080-06-13', reservation_duration_minutes=120))
        original = a.expect(201, 'POST', '/series', value, token, 'adoption')
        check(original['revision'] == 1 and original['interval_weeks'] == 1, 'initial series metadata')
        occurrences = original['occurrences']
        check([x['index'] for x in occurrences] == list(range(4)) and len({x['reference'] for x in occurrences}) == 4,
              'series indices/references')
        check(all(x['exception'] is False for x in occurrences), 'initial series exceptions')
        check(occurrences[0]['reservation'] == anchor, 'anchor regenerated')
        self.unchanged(anchor, saved_history)
        locals = model.local_occurrences(anchor['starts_at_local'], 4, 1)
        for i, occurrence in enumerate(occurrences):
            row = occurrence['reservation']; current_shape(row)
            check(row['reference'] == occurrence['reference'] and row['starts_at_local'] == locals[i], 'calendar series schedule')
            if i:
                check(row['revision'] == 1 and row['accepted_terms'] == model.selected(self.r, self.publications, locals[i][:10]), 'per-occurrence terms')
                check(a.history(row['reference'], token)[0]['event'] == 'created', 'generated occurrence history')
        sid = original['series_id']; target = occurrences[1]['reference']
        series_path = '/series/' + sid
        a.expect(200, 'PATCH', '/reservations/' + target, {'party_size': 2}, token)
        check(a.expect(200, 'GET', series_path, token=token)['revision'] == 1, 'no-op series increment')
        a.expect(200, 'PATCH', '/reservations/' + target, {'party_size': 3}, token)
        state = a.expect(200, 'GET', series_path, token=token)
        check(state['revision'] == 2 and state['occurrences'][1]['exception'] is True, 'real change not permanent exception')
        a.expect(200, 'PATCH', '/reservations/' + target, {'party_size': 2}, token)
        state = a.expect(200, 'GET', series_path, token=token)
        check(state['revision'] == 3 and state['occurrences'][1]['exception'] is True, 'reversion erased exception')
        a.expect(200, 'POST', '/reservations/' + anchor['reference'] + '/cancel', token=token)
        state = a.expect(200, 'GET', series_path, token=token)
        check(state['revision'] == 4 and state['occurrences'][0]['exception'] is False
              and all(x['reservation']['status'] == 'confirmed' for x in state['occurrences'][1:]), 'anchor cancel cascaded/exception')
        a.expect(200, 'POST', '/reservations/' + anchor['reference'] + '/cancel', token=token)
        check(a.expect(200, 'GET', series_path, token=token) == state, 'repeat cancellation series increment')
        check(a.expect(200, 'POST', '/series', value, token, 'adoption') == original, 'historical adoption receipt changed')
        check(a.book(token, body, 'create', 200) == anchor, 'anchor create receipt changed')
        for caller in [None, 'unknown', a.login('bob')]:
            a.expect(404, 'GET', series_path, token=caller, code='not_found')

    def series_validation_atomic_failure(self):
        a, token = self.fresh()
        anchor, _ = self.book()
        value = {'anchor_reference': anchor['reference'], 'count': 2, 'interval_weeks': 1}
        for field, bads in [('count', [1, 13, True, '2', 2.5]), ('interval_weeks', [0, 5, False, '1', 1.5])]:
            for bad in bads:
                a.expect(422, 'POST', '/series', {**value, field: bad}, token, 'reusable', 'validation_failed')
        a.expect(401, 'POST', '/series', value, key='anonymous', code='unauthenticated')
        a.expect(404, 'POST', '/series', value, a.login('bob'), 'foreign', 'not_found')
        blocker, _ = self.book(day='2080-06-13', key='blocker')
        snapshot = a.reservations(token); history = a.history(anchor['reference'], token)
        a.expect(409, 'POST', '/series', value, token, 'reusable', 'table_unavailable')
        check(a.reservations(token) == snapshot, 'partial failed adoption records')
        self.unchanged(anchor, history)
        a.expect(200, 'POST', '/reservations/' + blocker['reference'] + '/cancel', token=token)
        response = a.expect(201, 'POST', '/series', value, token, 'reusable')
        check(len(response['occurrences']) == 2, 'failed adoption consumed key')
        a.expect(409, 'POST', '/series', value, token, 'new-adoption', 'already_in_series')

    def series_dst_and_first_error(self):
        # Future spring anchors are editable; historical spring booking semantics
        # remain covered by the frozen inherited cases against the candidate.
        vectors = [('Europe/Berlin', '2027-03-21', '02:30', 'invalid_local_time'),
                   ('America/New_York', '2027-03-07', '02:30', 'invalid_local_time'),
                   ('Europe/Berlin', '2026-10-18', '02:30', None),
                   ('America/New_York', '2026-10-25', '01:30', None)]
        for zone, day, clock, error in vectors:
            a, token = self.fresh(model.fixture(zone=zone, opens='00:00', closes='05:00', duration=90))
            anchor, _ = self.book(day=day, at=clock)
            value = {'anchor_reference': anchor['reference'], 'count': 2, 'interval_weeks': 1}
            before = a.reservations(token)
            result = a.expect(422 if error else 201, 'POST', '/series', value, token, 'dst', error)
            if error:
                check(a.reservations(token) == before, 'DST failure left partial adoption')
            else:
                generated = result['occurrences'][1]['reservation']
                expected_local = model.local_occurrences(anchor['starts_at_local'], 2, 1)[1]
                expected = prior.resolve(expected_local, zone)
                check(generated['starts_at_local'] == expected_local and generated['starts_at'] == expected.isoformat(), 'recurring first fold')
                current_shape(generated)

    def collective_series_final_state(self):
        a, token = self.fresh()
        first, _ = self.book(table='z', key='one')
        second, _ = self.book(table='m', key='two')
        s1 = a.expect(201, 'POST', '/series', {'anchor_reference': first['reference'], 'count': 2, 'interval_weeks': 1}, token, 'series-one')
        s2 = a.expect(201, 'POST', '/series', {'anchor_reference': second['reference'], 'count': 2, 'interval_weeks': 1}, token, 'series-two')
        # Swap occupied single members and change another member in the first
        # series; both members cause one, not two, series counter increments.
        refs = [first['reference'], second['reference'], s1['occurrences'][1]['reference']]
        before = {r: a.current(r, token) for r in refs}
        histories = {r: a.history(r, token) for r in refs}
        value = {'moves': [{'reference': refs[0], 'table_id': 'm', 'expected_revision': 1},
                           {'reference': refs[1], 'table_id': 'z', 'expected_revision': 1},
                           {'reference': refs[2], 'party_size': 3, 'expected_revision': 1}]}
        receipt = a.expect(201, 'POST', '/reservation-moves', value, token, 'swap')
        check([r['reference'] for r in receipt['reservations']] == refs, 'batch response order')
        for ref in refs:
            current = a.current(ref, token)
            check(current['revision'] == 2, 'collective reservation delta')
            rows = a.history(ref, token)
            check(rows[:-1] == histories[ref] and rows[-1]['changes'] == model.changes(self.r, before[ref], current), 'collective actual-field history')
        states = [a.expect(200, 'GET', '/series/' + s['series_id'], token=token) for s in [s1, s2]]
        check([s['revision'] for s in states] == [2, 2], 'batch series increment per item')
        current_rows = a.reservations(token)
        a.expect(409, 'POST', '/reservation-moves', {'moves': [{'reference': refs[0], 'party_size': 1},
                                                            {'reference': refs[1], 'expected_revision': 1}]}, token, 'failed', 'stale_revision')
        check(a.reservations(token) == current_rows, 'failed collective partial records')
        check(a.expect(200, 'POST', '/reservation-moves', value, token, 'swap') == receipt, 'batch original receipt changed')
        for s, state in zip([s1, s2], states):
            check(a.expect(200, 'GET', '/series/' + s['series_id'], token=token) == state, 'replay/failure changed series')
        a.expect(201, 'POST', '/reservation-moves', {'moves': [{'reference': r} for r in refs]}, token, 'all-noop')
        check(a.reservations(token) == current_rows, 'all-noop batch changed records')

    def pause(self, source):
        check(self.control is not None, 'independent unavailable-source control required')
        marker = self.control / ('pause-' + source); marker.write_text('ready\n')
        deadline = time.monotonic() + 30
        while not (self.control / (source + '-unavailable')).exists():
            if time.monotonic() >= deadline:
                raise OSError('infrastructure control handshake expired')
            time.sleep(.1)

    def legacy_direct_upgrades(self):
        for version, source in self.legacy.items():
            check(source is not None, 'both independently started accepted legacy sources required')
            fx = model.fixture(); source.reset(fx)
            token = source.login(); second_token = source.login()
            body = prior.body('z')
            original = source.book(token, body, 'legacy-create')
            batch = {'moves': [{'reference': original['reference'], 'table_id': 'm'}]}
            old_batch = source.expect(201, 'POST', '/reservation-moves', batch, token, 'legacy-batch')
            snapshot = source.expect(200, 'GET', '/_test/export')
            self.pause('stage' + str(version))
            destination = self.dest
            destination.reset(fx); displaced = destination.login()
            destination.expect(204, 'POST', '/_test/import', snapshot)
            for session in [token, second_token]:
                current = destination.current(original['reference'], session)
                check(current['revision'] == 1 and current['accepted_terms'] == model.baseline(fx['restaurants'][0]), 'legacy known-state baseline')
                check(current['reservation_id'] == original['reservation_id'] and current['reference'] == original['reference']
                      and current['created_at'] == original['created_at'], 'legacy identity/timestamp changed')
            destination.expect(401, 'GET', '/reservations', token=displaced, code='unauthenticated')
            check(destination.book(token, body, 'legacy-create', 200) == original, 'legacy historical create shape changed')
            check(destination.expect(200, 'POST', '/reservation-moves', batch, token, 'legacy-batch') == old_batch, 'legacy historical batch shape changed')
            adopted = destination.expect(201, 'POST', '/series', {'anchor_reference': original['reference'], 'count': 2, 'interval_weeks': 1}, token, 'adopt-imported')
            check(adopted['occurrences'][0]['reference'] == original['reference'], 'legacy anchor adoption')
            self.third.expect(204, 'POST', '/_test/import', destination.expect(200, 'GET', '/_test/export'))
            check(self.third.book(token, body, 'legacy-create', 200) == original, 'legacy chained historical receipt')

    def native_snapshot_four_receipt_families(self):
        a, token = self.fresh()
        other_token = a.login()
        publication_body = {**model.policy(self.r, DAY), 'ignored': Decimal('1e309')}
        publication = self.publish(publication_body, 'publication')
        anchor, create_body = self.book(ids=['a', 'z'], party=6)
        adoption_body = {'anchor_reference': anchor['reference'], 'count': 3, 'interval_weeks': 1,
                         'ignored': Decimal('1e-1000')}
        adoption = a.expect(201, 'POST', '/series', adoption_body, token, 'adoption')
        child = adoption['occurrences'][1]['reference']
        batch_body = {'moves': [{'reference': child, 'table_ids': ['m', 'q'], 'party_size': 7}]}
        batch = a.expect(201, 'POST', '/reservation-moves', batch_body, token, 'batch')
        a.expect(200, 'POST', '/reservations/' + anchor['reference'] + '/cancel', token=token)
        a.expect(404, 'POST', '/reservations', prior.body('unknown'), token, 'failed-before-export', 'not_found')
        rows = a.reservations(token)
        histories = {r['reference']: a.history(r['reference'], token) for r in rows}
        series = a.expect(200, 'GET', '/series/' + adoption['series_id'], token=token)
        snapshot = a.expect(200, 'GET', '/_test/export')
        self.pause('source')
        d = self.dest
        d.reset(model.fixture()); displaced = d.login()
        for _ in range(2):
            d.expect(204, 'POST', '/_test/import', snapshot)
            check(d.reservations(token) == rows and d.reservations(other_token) == rows, 'native snapshot records/session continuity')
            check(d.expect(200, 'GET', '/restaurants/r/policies')['policies'] == self.publications, 'native immutable policy transfer')
            for ref in histories:
                check(d.history(ref, token) == histories[ref], 'native immutable history transfer')
            check(d.expect(200, 'GET', '/series/' + adoption['series_id'], token=token) == series, 'native series flags/revisions transfer')
            check(d.expect(200, 'POST', '/restaurants/r/policies', publication_body, token, 'publication') == publication, 'publication original transfer')
            check(d.book(token, create_body, 'create', 200) == anchor, 'create original transfer')
            check(d.expect(200, 'POST', '/series', adoption_body, token, 'adoption') == adoption, 'series original transfer')
            check(d.expect(200, 'POST', '/reservation-moves', batch_body, token, 'batch') == batch, 'collective original transfer')
            d.expect(401, 'GET', '/reservations', token=displaced, code='unauthenticated')
        for invalid in [{**snapshot, 'track': 'wrong'}, {**snapshot, 'format_version': 2}, {**snapshot, 'state': None}]:
            d.expect(422, 'POST', '/_test/import', invalid, code='validation_failed')
            check(d.reservations(token) == rows, 'invalid native import mutated records')
        chained = d.expect(200, 'GET', '/_test/export')
        self.pause('destination')
        self.third.expect(204, 'POST', '/_test/import', chained)
        check(self.third.reservations(token) == rows, 'source-unavailable A->B->C records')
        check(self.third.expect(200, 'POST', '/series', adoption_body, token, 'adoption') == adoption, 'A->B->C historical series receipt')
        self.third.book(token, prior.body('z', day='2080-08-01'), 'failed-before-export')
        self.third.reset(model.fixture())
        self.third.expect(401, 'GET', '/reservations', token=token, code='unauthenticated')

    def adoption_retry_concurrency_50(self):
        a, token = self.fresh()
        anchor, _ = self.book()
        value = {'anchor_reference': anchor['reference'], 'count': 12, 'interval_weeks': 4}
        before = a.history(anchor['reference'], token)
        responses = coordinated([lambda: a.request('POST', '/series', value, token, 'adopt-50') for _ in range(50)])
        check(sum(s == 201 for s, _ in responses) == 1 and sum(s == 200 for s, _ in responses) == 49,
              '50 adoption retries not exactly one effect')
        check(all(v == responses[0][1] for _, v in responses), '50 adoption originals differ')
        check(len(a.reservations(token)) == 12 and a.history(anchor['reference'], token) == before, '50 adoption duplicated records/changed anchor')
        series = responses[0][1]
        check(len(series['occurrences']) == 12 and [x['reservation']['starts_at_local'] for x in series['occurrences']]
              == model.local_occurrences(anchor['starts_at_local'], 12, 4), 'maximum count/interval calendar schedule')

    def batch_snapshot_coherence_50(self):
        a, token = self.fresh()
        one, _ = self.book(table='z', key='one')
        two, _ = self.book(table='m', key='two')
        value = {'moves': [{'reference': one['reference'], 'table_id': 'm'},
                           {'reference': two['reference'], 'table_id': 'z'}]}
        workers = [lambda: ('write', a.request('POST', '/reservation-moves', value, token, 'atomic-swap')) for _ in range(25)]
        workers += [lambda: ('snapshot', a.expect(200, 'GET', '/_test/export')) for _ in range(25)]
        results = coordinated(workers)
        writes = [v for kind, v in results if kind == 'write']
        check(sum(s == 201 for s, _ in writes) == 1 and sum(s == 200 for s, _ in writes) == 24, 'snapshot overlap retry allocations')
        receipt = writes[0][1]
        check(all(v == receipt for _, v in writes), 'snapshot-overlap batch originals differ')
        for kind, snapshot in results:
            if kind != 'snapshot':
                continue
            self.dest.expect(204, 'POST', '/_test/import', snapshot)
            rows = self.dest.reservations(token)
            by_ref = {r['reference']: r for r in rows}
            revisions = [by_ref[r['reference']]['revision'] for r in [one, two]]
            check(revisions in ([1, 1], [2, 2]), 'snapshot tore batch revisions')
            orientation = [by_ref[r['reference']]['table_id'] for r in [one, two]]
            check(orientation == (['z', 'm'] if revisions[0] == 1 else ['m', 'z']), 'snapshot tore batch occupancy')
            for r in [one, two]:
                history = self.dest.history(r['reference'], token)
                check(len(history) == revisions[0] and history[-1]['revision'] == revisions[0], 'snapshot tore history/record')
            if revisions[0] == 2:
                check(self.dest.expect(200, 'POST', '/reservation-moves', value, token, 'atomic-swap') == receipt,
                      'committed snapshot missing original receipt')
            else:
                self.dest.expect(201, 'POST', '/reservation-moves', value, token, 'atomic-swap')

    def run(self, names=None):
        for name in names or CASES:
            check(name in CASES, 'unknown prepared Stage 3 case')
            started = time.monotonic()
            try:
                getattr(self, name)()
                result = {'case': name, 'status': 'PASS'}
            except prior.CheckFailure as exc:
                result = {'case': name, 'status': 'FAIL', 'classification': 'PRODUCT DEFECT CANDIDATE', 'detail': str(exc)}
            except (OSError, TimeoutError) as exc:
                result = {'case': name, 'status': 'ERROR', 'classification': 'INCONCLUSIVE', 'detail': type(exc).__name__}
            except Exception as exc:
                result = {'case': name, 'status': 'ERROR', 'classification': 'VERIFIER DEFECT', 'detail': type(exc).__name__}
            result['seconds'] = round(time.monotonic() - started, 3)
            self.results.append(result); print(json.dumps(result), flush=True)
        timings = sum((a.timings for a in [self.api, self.dest, self.third, *self.legacy.values()] if a), [])
        return {'campaign': 'independent-stage-3-new-contract', 'cases': self.results,
                'all_passed': all(x['status'] == 'PASS' for x in self.results), 'requests': len(timings),
                'max_regular_seconds': max((v for p, v in timings if not p.startswith('/_test/')), default=0),
                'max_control_seconds': max((v for p, v in timings if p.startswith('/_test/')), default=0)}


CASES = ['permissions_policy_validation', 'effective_date_explanations', 'terms_history_noops_and_pairs',
         'revision_priority_and_concurrency', 'publication_concurrency_receipts',
         'series_anchor_and_exceptions', 'series_validation_atomic_failure',
         'series_dst_and_first_error', 'collective_series_final_state', 'legacy_direct_upgrades',
         'adoption_retry_concurrency_50', 'batch_snapshot_coherence_50', 'native_snapshot_four_receipt_families']


def main():
    p = argparse.ArgumentParser()
    p.add_argument('mode', choices=['calibrate', 'http'])
    for option in ['revision', 'source', 'destination', 'third', 'stage1', 'stage2', 'control', 'out']:
        p.add_argument('--' + option)
    p.add_argument('--released', action='store_true'); p.add_argument('--cases', nargs='+')
    args = p.parse_args()
    if args.mode == 'calibrate':
        print(json.dumps(model.calibrate())); return
    if not args.released or not re.fullmatch('[0-9a-f]{40}', args.revision or ''):
        p.error('Conductor exact FULL Stage 3 production SHA release required before candidate requests')
    report = Campaign(args.source, args.destination, args.third, args.stage1, args.stage2, args.control).run(args.cases)
    report['production_revision'] = args.revision
    if args.out:
        Path(args.out).write_text(json.dumps(report, indent=2) + '\n')
    raise SystemExit(0 if report['all_passed'] else 1)


if __name__ == '__main__':
    main()
