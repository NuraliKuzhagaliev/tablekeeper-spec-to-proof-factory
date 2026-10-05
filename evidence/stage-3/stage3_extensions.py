"""Explicit uncovered Stage 3 ledger procedures; independent HTTP expectations."""
import argparse
import copy
import datetime as dt
from decimal import Decimal
import json
from pathlib import Path
import re
import time

import stage3_campaign as core
import policy_oracle as model
import stage1_campaign as prior

check = prior.check
DAY = prior.DAY


def private_state(api):
    """Observe opaque counters/identities only; never reuse production decisions."""
    envelope = api.expect(200, 'GET', '/_test/export')
    state = envelope['state']
    if state.get('encoding') == 'tablekeeper-json-v1':
        return json.loads(state['payload'], parse_float=Decimal)
    return state


class Extensions(core.Campaign):
    def policy_limits_and_namespaces(self):
        fx = model.fixture(); other = copy.deepcopy(fx['restaurants'][0]); other['id'] = 'other'
        other['manager_user_ids'] = ['ada', 'bob']; fx['restaurants'].append(other)
        a, token = self.fresh(fx); bob = a.login('bob')
        p = model.policy(self.r, DAY)
        # Exact boundary publications need not have a bookable slot: both endpoints
        # are valid policy values independently of their chosen duration/opening.
        for key, slot, duration, cutoff, capacity in [('minimum', 1, 1, 0, 1), ('maximum', 1440, 1440, 10080, 100)]:
            self.publish({**p, 'slot_minutes': slot, 'reservation_duration_minutes': duration,
                          'cancellation_cutoff_minutes': cutoff,
                          'capacities': {t['id']: capacity for t in self.r['tables']}}, key)
        first = a.expect(201, 'POST', '/restaurants/other/policies', p, token, 'minimum')
        check(first['policy_version'] == 1, 'policy namespace not per restaurant/path')
        second = a.expect(201, 'POST', '/restaurants/other/policies', p, bob, 'minimum')
        check(second['policy_version'] == 2, 'policy namespace not per user')
        a.expect(409, 'POST', '/restaurants/other/policies', {'effective_from': False}, bob, 'minimum', 'idempotency_key_reuse')
        third = a.expect(201, 'POST', '/restaurants/other/policies', {**p, 'timezone': 'wrong', 'tables': [], 'combinable': []}, bob, 'x' * 255)
        check(third['policy_version'] == 3, 'valid longest key/version')
        original_detail = a.expect(200, 'GET', '/restaurants/other')
        check(original_detail['timezone'] == other['timezone'] and original_detail['tables'] == other['tables']
              and original_detail['combinable'] == other['combinable'], 'ignored fields modified immutable identity')
        for raw in [b'NaN', b'Infinity', b'{"ignored":NaN}', b'[1]', b'{']:
            a.expect(400, 'POST', '/restaurants/r/policies', token=token, key='malformed', raw=raw, code='malformed_request')
        for invalid in [{**p, 'opening_hours': None}, {**p, 'opening_hours': 'hours'},
                        {**p, 'opening_hours': [{'weekday': 'mon', 'opens': '18:60', 'closes': '23:00'}]},
                        {**p, 'opening_hours': [{'weekday': 'mon', 'opens': '18:00', 'closes': '18:00'}]},
                        {**p, 'capacities': {'z': 4, 'a': 2, 'm': 6}},
                        {**p, 'capacities': {t['id']: None for t in self.r['tables']}}]:
            old = a.expect(200, 'GET', '/restaurants/r/policies')
            a.expect(422, 'POST', '/restaurants/r/policies', invalid, token, 'invalid', 'validation_failed')
            check(a.expect(200, 'GET', '/restaurants/r/policies') == old, 'invalid recognized policy shape changed version')

    def accepted_cutoff_and_stale_precedence(self):
        fx = model.fixture(zone='UTC'); r = fx['restaurants'][0]
        r['cancellation_cutoff_minutes'] = 10080
        a, token = self.fresh(fx)
        clock = dt.datetime.now(dt.timezone.utc).replace(second=0, microsecond=0) + dt.timedelta(days=2)
        day = clock.date().isoformat()
        row, _ = self.book(day=day, at='18:00')
        history = a.history(row['reference'], token)
        self.publish(model.policy(self.r, day, cancellation_cutoff_minutes=0))
        path = '/reservations/' + row['reference']
        a.expect(409, 'POST', path + '/cancel', token=token, code='cutoff_passed')
        a.expect(409, 'PATCH', path, {'party_size': 'bad'}, token, code='cutoff_passed')
        a.expect(409, 'PATCH', path, {}, token, code='cutoff_passed')
        a.expect(409, 'PATCH', path, {'expected_revision': 2, 'party_size': 'bad'}, token, code='stale_revision')
        a.expect(422, 'PATCH', path, {'expected_revision': True}, token, code='validation_failed')
        self.unchanged(row, history)
        a.expect(409, 'POST', '/series', {'anchor_reference': row['reference'], 'count': 2, 'interval_weeks': 1}, token, 'cutoff', 'cutoff_passed')
        a.expect(409, 'POST', '/reservation-moves', {'moves': [{'reference': row['reference'], 'expected_revision': 2, 'party_size': False}]}, token, 'stale', 'stale_revision')
        self.unchanged(row, history)
        # Reverse direction: old accepted zero must allow cancellation even after
        # publishing a seven-day window that would currently forbid it.
        fx['restaurants'][0]['cancellation_cutoff_minutes'] = 0
        a, token = self.fresh(fx); row, _ = self.book(day=day)
        self.publish(model.policy(self.r, day, cancellation_cutoff_minutes=10080))
        check(a.expect(200, 'POST', '/reservations/' + row['reference'] + '/cancel', token=token)['status'] == 'cancelled', 'cancel used new cutoff')

    def complete_result_grid_duration_and_history(self):
        a, token = self.fresh()
        first, _ = self.book(at='18:30'); ref = first['reference']
        original_history = a.history(ref, token)
        self.publish(model.policy(self.r, DAY, slot_minutes=60))
        a.expect(422, 'PATCH', '/reservations/' + ref, {'party_size': 3}, token, code='not_on_slot_grid')
        self.unchanged(first, original_history)
        check(a.expect(200, 'PATCH', '/reservations/' + ref, {'party_size': 2}, token) == first, 'no-op checked newly incompatible grid')
        # Party-only real change lengthens the accepted interval and conflicts
        # with a booking that was adjacent under the retained 90-minute terms.
        a, token = self.fresh(); first, _ = self.book(); ref = first['reference']
        adjacent, _ = self.book(at='19:30', key='adjacent')
        saved = a.history(ref, token)
        self.publish(model.policy(self.r, DAY, reservation_duration_minutes=120))
        a.expect(409, 'PATCH', '/reservations/' + ref, {'party_size': 3}, token, code='table_unavailable')
        self.unchanged(first, saved)
        a.expect(200, 'POST', '/reservations/' + adjacent['reference'] + '/cancel', token=token)
        previous = first
        for patch in [{'table_id': 'm'}, {'starts_at_local': DAY + 'T18:30'}, {'party_size': 4},
                      {'table_ids': ['a', 'z'], 'starts_at_local': DAY + 'T19:00', 'party_size': 5},
                      {'table_id': 'm', 'starts_at_local': DAY + 'T19:30', 'party_size': 3}]:
            result = a.expect(200, 'PATCH', '/reservations/' + ref, patch, token)
            core.current_shape(result)
            rows = a.history(ref, token)
            check(rows[-1]['changes'] == model.changes(self.r, previous, result), 'actual-field history/order')
            check(result['revision'] == previous['revision'] + 1 and rows[-1]['revision'] == result['revision'], 'one real-change revision')
            previous = result
        check([r['seq'] for r in a.history(ref, token)] == list(range(1, 7)), 'immediate writes lose sequence')
        for patch in [{'table_id': 'm'}, {'table_ids': ['m']}, {'party_size': 3, 'expected_revision': 6}]:
            before = a.history(ref, token)
            check(a.expect(200, 'PATCH', '/reservations/' + ref, patch, token) == previous, 'explicit same-value no-op changes snapshot')
            check(a.history(ref, token) == before, 'same-value history event')
        cancelled = a.expect(200, 'POST', '/reservations/' + ref + '/cancel', token=token)
        check(a.expect(200, 'GET', '/reservations/' + ref + '/decision', token=token)['revision'] == cancelled['revision'], 'cancelled decision stale')
        a.expect(409, 'PATCH', '/reservations/' + ref, {}, token, code='reservation_cancelled')

    def recurrence_first_failure_and_calendar_bounds(self):
        a, token = self.fresh()
        anchor, _ = self.book(ids=['a', 'z'], party=6)
        # Index 1 overlap must win over index 2's capacity failure.
        blocker, _ = self.book(table='a', day='2080-06-13', key='blocker')
        self.publish(model.policy(self.r, '2080-06-20', capacities={t['id']: 1 for t in self.r['tables']}))
        body = {'anchor_reference': anchor['reference'], 'count': 4, 'interval_weeks': 1}
        before = private_state(a)
        a.expect(409, 'POST', '/series', body, token, 'first-index', 'table_unavailable')
        check(private_state(a) == before, 'first-index failure retained any private state/key/counter')
        a.expect(200, 'POST', '/reservations/' + blocker['reference'] + '/cancel', token=token)
        before = private_state(a)
        a.expect(422, 'POST', '/series', body, token, 'first-index', 'party_exceeds_capacity')
        check(private_state(a) == before, 'later policy failure partial series')
        self.publish(model.policy(self.r, '2080-06-20'))
        result = a.expect(201, 'POST', '/series', body, token, 'first-index')
        check(len(result['occurrences']) == 4, 'failed first-index key not reusable')
        # Last representable date is valid as an ordinary booking, but generation
        # beyond it must reject without partial data or an internal error.
        a, token = self.fresh(model.fixture(zone='UTC'))
        anchor, _ = self.book(day='9999-12-31')
        before = private_state(a)
        a.expect(422, 'POST', '/series', {'anchor_reference': anchor['reference'], 'count': 2, 'interval_weeks': 1}, token, 'terminal', 'validation_failed')
        check(private_state(a) == before, 'terminal-date adoption changed state')
        # Missing/shape keys are isolated from resource eligibility ties.
        for body in [{}, {'anchor_reference': anchor['reference'], 'count': 2},
                     {'anchor_reference': anchor['reference'], 'interval_weeks': 1},
                     {'anchor_reference': 123, 'count': 2, 'interval_weeks': 1}]:
            expected = 400 if body.get('anchor_reference') == 123 else 422
            a.expect(expected, 'POST', '/series', body, token, 'missing', 'malformed_request' if expected == 400 else 'validation_failed')

    def explicit_restaurant_and_affected_series_deltas(self):
        a, token = self.fresh()
        rows = []
        for table in ['z', 'm', 'q']:
            row, _ = self.book(table=table, party=1, key='anchor-' + table); rows.append(row)
        start_counter = private_state(a)['restaurant_revisions']['r']
        series = []
        for i, row in enumerate(rows):
            value = {'anchor_reference': row['reference'], 'count': 2, 'interval_weeks': 1}
            series.append(a.expect(201, 'POST', '/series', value, token, 'series-' + str(i)))
            check(private_state(a)['restaurant_revisions']['r'] == start_counter + i + 1, 'adoption restaurant counter not once')
        # Two real members of A, one of B, unchanged C. All capacities >=2 except
        # q still2; selected slots/table identities do not otherwise change.
        moves = [{'reference': x['reference'], 'party_size': 2} for x in series[0]['occurrences']]
        moves += [{'reference': series[1]['occurrences'][0]['reference'], 'party_size': 2},
                  {'reference': series[2]['occurrences'][0]['reference']}]
        before = private_state(a); value = {'moves': moves}
        receipt = a.expect(201, 'POST', '/reservation-moves', value, token, 'counter-batch')
        after = private_state(a)
        check(after['restaurant_revisions']['r'] == before['restaurant_revisions']['r'] + 1, 'real batch restaurant counter per item')
        states = [a.expect(200, 'GET', '/series/' + s['series_id'], token=token) for s in series]
        check([s['revision'] for s in states] == [2, 2, 1], 'unchanged-only series/counter deltas')
        check([x['exception'] for x in states[0]['occurrences']] == [True, True]
              and [x['exception'] for x in states[1]['occurrences']] == [True, False]
              and not any(x['exception'] for x in states[2]['occurrences']), 'collective permanent exceptions')
        check(a.expect(200, 'POST', '/reservation-moves', value, token, 'counter-batch') == receipt, 'counter batch historical replay')
        check(private_state(a) == after, 'counter batch replay changed private state')
        noop = {'moves': [{'reference': m['reference']} for m in moves]}
        a.expect(201, 'POST', '/reservation-moves', noop, token, 'noop-counter')
        after_noop = private_state(a)
        check(after_noop['restaurant_revisions'] == after['restaurant_revisions'], 'all-noop restaurant counter')
        check([a.expect(200, 'GET', '/series/' + s['series_id'], token=token) for s in series] == states, 'all-noop affected-series increment')
        a.expect(409, 'POST', '/reservation-moves', {'moves': [{'reference': moves[0]['reference'], 'party_size': 3},
                                                            {'reference': moves[1]['reference'], 'expected_revision': 1}]}, token, 'failed-counter', 'stale_revision')
        check(private_state(a) == after_noop, 'failed batch altered private counters/flags/receipts')

    def local_date_selection_and_privacy_baselines(self):
        fx = model.fixture(zone='Pacific/Kiritimati', opens='00:00', closes='05:00')
        a, token = self.fresh(fx)
        self.publish(model.policy(self.r, '2080-06-06', reservation_duration_minutes=60))
        row, _ = self.book(at='00:00')
        check(row['accepted_terms']['policy_version'] == 1, 'selection used UTC previous day')
        check(prior.instant_seconds(row['starts_at']) < prior.instant_seconds(DAY + 'T00:00:00+00:00'), 'fixture does not cross UTC date')
        bob = a.login('bob'); unknown = 'ZZZZZZ'
        for suffix in ['/history', '/decision']:
            for ref in [row['reference'], unknown]:
                for caller in [None, '', 'unknown', bob]:
                    a.expect(404, 'GET', '/reservations/' + ref + suffix, token=caller, code='not_found')
        a.expect(401, 'GET', '/reservations/' + row['reference'], code='unauthenticated')
        # Manager privilege never grants access to a bob-owned reservation.
        foreign = a.book(bob, prior.body('m', at='00:00'), 'bob-owned')
        for suffix in ['', '/history', '/decision']:
            a.expect(404, 'GET', '/reservations/' + foreign['reference'] + suffix, token=token, code='not_found')

    def policy_batch_input_order_and_retained_noop(self):
        a, token = self.fresh()
        one, _ = self.book(); two, _ = self.book(table='m', key='two')
        h1 = a.history(one['reference'], token)
        self.publish(model.policy(self.r, DAY, reservation_duration_minutes=120,
                                  capacities={**model.baseline(self.r)['capacities'], 'z': 1}))
        body = {'moves': [{'reference': one['reference']}, {'reference': two['reference'], 'party_size': 3}]}
        receipt = a.expect(201, 'POST', '/reservation-moves', body, token, 'mixed-noop')
        check(receipt['reservations'][0] == one and a.history(one['reference'], token) == h1, 'listed no-op adopted incompatible new terms')
        changed = receipt['reservations'][1]
        check(changed['revision'] == 2 and changed['accepted_terms']['policy_version'] == 1, 'real batch did not adopt complete selected policy')
        before = private_state(a)
        # A first candidate occupancy conflict cannot mask a later item's stale
        # control error. Stale/control precedence remains per input item.
        failure = {'moves': [{'reference': one['reference'], 'table_id': 'm'},
                             {'reference': two['reference'], 'expected_revision': 1}]}
        a.expect(409, 'POST', '/reservation-moves', failure, token, 'priority', 'stale_revision')
        check(private_state(a) == before, 'input-priority failure retained state/key')
        failure['moves'].reverse()
        a.expect(409, 'POST', '/reservation-moves', failure, token, 'priority', 'stale_revision')
        check(private_state(a) == before, 'input-priority reordered failure retained state')
        # Successful historical receipt resolves before now-stale per-item state.
        check(a.expect(200, 'POST', '/reservation-moves', body, token, 'mixed-noop') == receipt, 'batch replay re-ran current validation')
        a.expect(409, 'POST', '/reservation-moves', {'moves': []}, token, 'mixed-noop', 'idempotency_key_reuse')

    def series_reordered_dates_cancelled_exceptions(self):
        a, token = self.fresh()
        anchor, _ = self.book()
        value = {'anchor_reference': anchor['reference'], 'count': 3, 'interval_weeks': 1}
        original = a.expect(201, 'POST', '/series', value, token, 'series')
        sid = original['series_id']; path = '/series/' + sid
        child = original['occurrences'][2]['reference']
        a.expect(200, 'PATCH', '/reservations/' + child, {'starts_at_local': '2080-06-05T18:00'}, token)
        state = a.expect(200, 'GET', path, token=token)
        check([x['index'] for x in state['occurrences']] == [0, 1, 2]
              and [x['reference'] for x in state['occurrences']] == [x['reference'] for x in original['occurrences']], 'date change renumbered recurring identities')
        check(state['occurrences'][2]['exception'] is True and state['revision'] == 2, 'date change not permanent exception')
        a.expect(200, 'POST', '/reservations/' + child + '/cancel', token=token)
        state = a.expect(200, 'GET', path, token=token)
        check(state['revision'] == 3 and state['occurrences'][2]['exception'] is True, 'cancel erased existing exception')
        before = private_state(a)
        a.expect(200, 'POST', '/reservations/' + child + '/cancel', token=token)
        check(private_state(a) == before, 'repeat cancelled exception changed private state')
        a.expect(409, 'PATCH', '/reservations/' + child, {'party_size': 3}, token, code='reservation_cancelled')
        check(private_state(a) == before, 'failed cancelled occurrence edit changed flags')
        check(a.expect(200, 'POST', '/series', value, token, 'series') == original, 'reordered/cancelled series changed original receipt')
        a.expect(404, 'GET', '/series/unknown-series', token=token, code='not_found')
        a.reservations(token)
        a, token = self.fresh(); anchor, _ = self.book()
        a.expect(200, 'POST', '/reservations/' + anchor['reference'] + '/cancel', token=token)
        a.expect(409, 'POST', '/series', {'anchor_reference': anchor['reference'], 'count': 2, 'interval_weeks': 1}, token, 'cancelled-anchor', 'reservation_cancelled')

    def mixed_policy_patch_cancel_serial_oracle(self):
        observations = []
        for iteration in range(8):
            a, token = self.fresh(); original, _ = self.book(); ref = original['reference']
            publication = model.policy(self.r, DAY, reservation_duration_minutes=120)
            patch = {'party_size': 3}
            def transition(state, operation):
                state = copy.deepcopy(state); row = state['row']
                if operation == 'publication':
                    value = {**publication, 'policy_version': 1}; state['policies'] = [value]
                    return state, (201, value)
                if operation == 'patch':
                    error, result, delta = model.amend(self.r, state['policies'], row, patch, 0)
                    if error:
                        return state, (409, error)
                    state['row'] = result
                    state['events'].append(('changed', delta, result['revision'], result['accepted_terms']))
                    return state, (200, result)
                if row['status'] == 'confirmed':
                    row['status'] = 'cancelled'; row['revision'] += 1
                    state['events'].append(('cancelled', [], row['revision'], row['accepted_terms']))
                return state, (200, row)
            initial = {'row': original, 'policies': [], 'events': [('created', model.changes(self.r, None, original), 1, original['accepted_terms'])]}
            permitted = model.serial_outcomes(initial, ['publication', 'patch', 'cancel'], transition)
            actual = core.coordinated([lambda: a.request('POST', '/restaurants/r/policies', publication, token, 'publication'),
                                       lambda: a.request('PATCH', '/reservations/' + ref, patch, token),
                                       lambda: a.request('POST', '/reservations/' + ref + '/cancel', token=token)])
            row = a.current(ref, token); history = a.history(ref, token)
            def normalize(response):
                status, value = response
                if isinstance(value, str):
                    return status, value
                if isinstance(value, dict) and 'error' in value:
                    return status, value['error']['code']
                return status, value
            actual_events = [(x['event'], x['changes'], x['revision'], x['accepted_terms']) for x in history]
            matched = any(state['row'] == row and state['events'] == actual_events
                          and all(normalize(actual[i]) == normalize(responses[i]) for i in range(3))
                          for state, responses in permitted)
            check(matched, 'policy/patch/cancel concurrent result not any six-order serialization')
            observations.append({'iteration': iteration, 'orders_considered': 6, 'matched': True})
        self.serial_observations = observations

    def series_keys_policy_grid_and_closed_occurrences(self):
        a, token = self.fresh()
        anchor, _ = self.book(key='shared')
        body = {'anchor_reference': anchor['reference'], 'count': 2, 'interval_weeks': 1}
        a.expect(400, 'POST', '/series', body, token, code='missing_idempotency_key')
        a.expect(422, 'POST', '/series', body, token, 'x' * 256, 'validation_failed')
        for field in ['count', 'interval_weeks']:
            for invalid in [None, [], {}]:
                a.expect(422, 'POST', '/series', {**body, field: invalid}, token, 'failed-shape', 'validation_failed')
        original = a.expect(201, 'POST', '/series', {**body, 'ignored': Decimal('1e309')}, token, 'shared')
        check(a.expect(200, 'POST', '/series', {**body, 'ignored': Decimal('10e308')}, token, 'shared') == original,
              'series exact equivalent numeric replay')
        a.expect(409, 'POST', '/series', {'count': False}, token, 'shared', 'idempotency_key_reuse')
        bob = a.login('bob'); foreign = a.book(bob, prior.body('m'), 'shared')
        second = a.expect(201, 'POST', '/series', {'anchor_reference': foreign['reference'], 'count': 2, 'interval_weeks': 1}, bob, 'shared')
        check(second['series_id'] != original['series_id'], 'series receipt namespace crosses owners')
        for kind, changes, error in [('grid', {'slot_minutes': 60}, 'not_on_slot_grid'),
                                     ('closed', {'opening_hours': []}, 'outside_opening_hours')]:
            a, token = self.fresh(); anchor, _ = self.book(at='18:30')
            self.publish(model.policy(self.r, '2080-06-13', **changes))
            before = private_state(a)
            a.expect(422, 'POST', '/series', {'anchor_reference': anchor['reference'], 'count': 3, 'interval_weeks': 1}, token, 'x' * 255, error)
            check(private_state(a) == before, 'generated ' + kind + ' rejection changes state/claim')
            query = '/availability?restaurant_id=r&date=2080-06-13&party_size=2&explain=true'
            check(a.expect(200, 'GET', query)['slots'] == model.slots(self.r, self.publications, '2080-06-13', 2, explain=True),
                  'published grid/closed explanation oracle')
            self.publish(model.policy(self.r, '2080-06-13'))
            a.expect(201, 'POST', '/series', {'anchor_reference': anchor['reference'], 'count': 3, 'interval_weeks': 1}, token, 'x' * 255)

    def amended_pair_anchor_and_legacy_history_baselines(self):
        a, token = self.fresh()
        old, old_body = self.book(key='old-original')
        current = a.expect(200, 'PATCH', '/reservations/' + old['reference'],
                           {'table_ids': ['z', 'a'], 'party_size': 6, 'starts_at_local': '2080-06-07T18:30'}, token)
        history = a.history(old['reference'], token)
        self.publish(model.policy(self.r, '2080-06-20', reservation_duration_minutes=120))
        body = {'anchor_reference': old['reference'], 'count': 12, 'interval_weeks': 4}
        response = a.expect(201, 'POST', '/series', body, token, 'amended-pair-adoption')
        check(response['occurrences'][0]['reservation'] == current and a.history(old['reference'], token) == history,
              'adoption regenerated amended anchor metadata/history')
        check(a.book(token, old_body, 'old-original', 200) == old, 'amended pair adoption changed pre-amendment original receipt')
        locals = model.local_occurrences(current['starts_at_local'], 12, 4)
        for index, occurrence in enumerate(response['occurrences']):
            row = occurrence['reservation']; core.current_shape(row)
            check(row['starts_at_local'] == locals[index] and row['table_ids'] == ['a', 'z'] and row['party_size'] == 6,
                  'generated occurrence copied original rather than current anchor intent')
            if index:
                check(row['accepted_terms'] == model.selected(self.r, self.publications, locals[index][:10]) and row['revision'] == 1,
                      'generated policy/initial revision for amended anchor')
        for version, legacy in self.legacy.items():
            fx = model.fixture(); legacy.reset(fx); old_token = legacy.login()
            old_create = legacy.book(old_token, prior.body(), 'legacy-original')
            migrated_record = legacy.expect(200, 'PATCH', '/reservations/' + old_create['reference'], {'table_id': 'm'}, old_token)
            cancelled = legacy.book(old_token, prior.body('z', at='20:00'), 'legacy-cancelled')
            legacy.expect(200, 'POST', '/reservations/' + cancelled['reference'] + '/cancel', token=old_token)
            self.dest.expect(204, 'POST', '/_test/import', legacy.expect(200, 'GET', '/_test/export'))
            reference = old_create['reference']; current = self.dest.current(reference, old_token)
            baseline = self.dest.expect(200, 'GET', '/reservations/' + reference + '/history', token=old_token)
            check(baseline['entries'] == [] and baseline['provenance']['kind'] == 'legacy_baseline'
                  and baseline['provenance']['known_state'] == current, 'legacy migration invented history or changed known state')
            check(current['table_id'] == migrated_record['table_id'] and current['created_at'] == migrated_record['created_at'],
                  'legacy amended known facts changed')
            self.dest.expect(200, 'PATCH', '/reservations/' + reference, {'party_size': 3}, old_token)
            future = self.dest.expect(200, 'GET', '/reservations/' + reference + '/history', token=old_token)
            check(future['provenance'] == baseline['provenance'] and len(future['entries']) == 1
                  and future['entries'][0]['seq'] == 1 and future['entries'][0]['event'] == 'changed'
                  and future['entries'][0]['changes'] == [{'field': 'party_size', 'from': 2, 'to': 3}],
                  'post-migration event fabricated earlier timeline')
            cancelled_history = self.dest.expect(200, 'GET', '/reservations/' + cancelled['reference'] + '/history', token=old_token)
            check(cancelled_history['entries'] == [] and cancelled_history['provenance']['known_state']['status'] == 'cancelled',
                  'legacy cancelled baseline invented events')
            check(self.dest.book(old_token, prior.body(), 'legacy-original', 200) == old_create,
                  'legacy known-state augmentation rewrote old original JSON')


CASES = ['policy_limits_and_namespaces', 'accepted_cutoff_and_stale_precedence',
         'complete_result_grid_duration_and_history', 'recurrence_first_failure_and_calendar_bounds',
         'explicit_restaurant_and_affected_series_deltas', 'local_date_selection_and_privacy_baselines',
         'policy_batch_input_order_and_retained_noop', 'series_reordered_dates_cancelled_exceptions',
         'mixed_policy_patch_cancel_serial_oracle', 'series_keys_policy_grid_and_closed_occurrences']
CASES.append('amended_pair_anchor_and_legacy_history_baselines')


def main():
    p = argparse.ArgumentParser(); p.add_argument('--released', action='store_true'); p.add_argument('--revision', required=True)
    for name in ['source', 'destination', 'third', 'stage1', 'stage2', 'control', 'out']:
        p.add_argument('--' + name)
    p.add_argument('--cases', nargs='+'); args = p.parse_args()
    if not args.released or not re.fullmatch('[0-9a-f]{40}', args.revision):
        p.error('explicit FULL Stage 3 release required')
    campaign = Extensions(args.source, args.destination, args.third, args.stage1, args.stage2, args.control)
    for name in args.cases or CASES:
        check(name in CASES, 'unknown extension case'); started = time.monotonic()
        try:
            getattr(campaign, name)(); result = {'case': name, 'status': 'PASS'}
        except prior.CheckFailure as error:
            result = {'case': name, 'status': 'FAIL', 'classification': 'PRODUCT DEFECT CANDIDATE', 'detail': str(error)}
        except Exception as error:
            result = {'case': name, 'status': 'ERROR', 'classification': 'INCONCLUSIVE', 'detail': type(error).__name__}
        result['seconds'] = round(time.monotonic() - started, 3); campaign.results.append(result)
        print(json.dumps(result), flush=True)
    timings = campaign.api.timings + campaign.dest.timings + campaign.third.timings
    report = {'production_revision': args.revision, 'cases': campaign.results,
              'all_passed': all(x['status'] == 'PASS' for x in campaign.results), 'requests': len(timings),
              'max_regular_seconds': max((v for p, v in timings if not p.startswith('/_test/')), default=0),
              'max_control_seconds': max((v for p, v in timings if p.startswith('/_test/')), default=0)}
    Path(args.out).write_text(json.dumps(report, indent=2) + '\n')
    raise SystemExit(0 if report['all_passed'] else 1)


if __name__ == '__main__':
    main()
