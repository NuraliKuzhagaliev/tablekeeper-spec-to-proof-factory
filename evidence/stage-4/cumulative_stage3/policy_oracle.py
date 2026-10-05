"""Specification-derived Stage 3 model. No production modules or algorithms."""
import copy
import datetime as dt
from fractions import Fraction
from itertools import permutations
from pathlib import Path
import sys
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).parent / 'cumulative'))
import stage1_campaign as prior
import oracle as pairs

FIELDS = ('slot_minutes', 'reservation_duration_minutes', 'cancellation_cutoff_minutes',
          'opening_hours', 'capacities')


def fixture(**kwargs):
    value = pairs.fixture(**kwargs)
    value['restaurants'][0]['manager_user_ids'] = ['ada']
    return value


def baseline(restaurant):
    return dict(policy_version=0,
                **{k: copy.deepcopy(restaurant[k]) for k in FIELDS if k != 'capacities'},
                capacities={t['id']: t['capacity'] for t in restaurant['tables']})


def policy(restaurant, date, **changes):
    value = baseline(restaurant)
    del value['policy_version']
    return dict(value, effective_from=date, **changes) if not changes else {
        **value, 'effective_from': date, **changes}


def selected(restaurant, publications, date):
    eligible = [p for p in publications if p['effective_from'] <= date]
    if not eligible:
        return baseline(restaurant)
    chosen = max(eligible, key=lambda p: (p['effective_from'], p['policy_version']))
    return {k: copy.deepcopy(chosen[k]) for k in ('policy_version', *FIELDS)}


def members(restaurant, value):
    ids = value.get('table_ids', [value.get('table_id')])
    if len(ids) == 1:
        return list(ids)
    for declared in restaurant.get('combinable', []):
        if len(ids) == 2 and set(ids) == set(declared):
            return list(declared)
    raise ValueError('combination_not_allowed')


def changes(restaurant, before, after):
    old = members(restaurant, before) if before else None
    new = members(restaurant, after)
    result = []
    if old != new:
        pair = len(new) > 1 or (old is not None and len(old) > 1)
        result.append({'field': 'table_ids' if pair else 'table_id',
                       'from': old if pair else old[0] if old else None,
                       'to': new if pair else new[0]})
    for field in ('starts_at_local', 'party_size'):
        previous = before[field] if before else None
        if previous != after[field]:
            result.append({'field': field, 'from': previous, 'to': after[field]})
    return result


def local_occurrences(local, count, interval):
    date, clock = local.split('T')
    anchor = dt.date.fromisoformat(date)
    return [(anchor + dt.timedelta(days=i * interval * 7)).isoformat() + 'T' + clock
            for i in range(count)]


def rules(restaurant, terms, local, party, occupied):
    start = prior.resolve(local, restaurant['timezone'])
    if start is None:
        raise ValueError('invalid_local_time')
    a = prior.instant_seconds(start.isoformat())
    b = a + int(terms['reservation_duration_minutes']) * 60
    result = []
    for table in restaurant['tables']:
        capacity = Fraction(terms['capacities'][table['id']]) >= Fraction(party)
        free = not any(r['restaurant_id'] == restaurant['id'] and r['status'] == 'confirmed'
                       and table['id'] in pairs.members(r)
                       and prior.overlaps(a, b, prior.instant_seconds(r['starts_at']),
                                          prior.instant_seconds(r['ends_at'])) for r in occupied)
        result.append({'table_id': table['id'], 'policy_version': terms['policy_version'],
                       'available': capacity and free,
                       'rules': [{'rule': 'capacity', 'holds': capacity},
                                 {'rule': 'no_overlap', 'holds': free}]})
    return result


def slots(restaurant, publications, date, party, occupied=(), explain=False):
    terms = selected(restaurant, publications, date)
    effective = copy.deepcopy(restaurant)
    effective.update({k: terms[k] for k in FIELDS if k != 'capacities'})
    for table in effective['tables']:
        table['capacity'] = terms['capacities'][table['id']]
    result = pairs.slots({'restaurants': [effective]}, date, party, occupied)
    if explain:
        for slot in result:
            slot['explain'] = rules(restaurant, terms, slot['starts_at_local'], party, occupied)
    return result


def validate_result(restaurant, terms, record):
    """Independent non-occupancy validation for synthetic model fixtures."""
    local = record['starts_at_local']
    start = prior.resolve(local, restaurant['timezone'])
    if start is None:
        return 'invalid_local_time'
    date, clock = local.split('T')
    weekday = prior.WEEK[dt.date.fromisoformat(date).weekday()]
    opening = next((h for h in terms['opening_hours'] if h['weekday'] == weekday), None)
    if opening is None:
        return 'outside_opening_hours'
    minutes = lambda x: int(x[:2]) * 60 + int(x[3:])
    close = prior.resolve(date + 'T' + opening['closes'], restaurant['timezone'])
    if (clock < opening['opens'] or close is None
            or prior.instant_seconds(start.isoformat()) + terms['reservation_duration_minutes'] * 60
            > prior.instant_seconds(close.isoformat())):
        return 'outside_opening_hours'
    if (minutes(clock) - minutes(opening['opens'])) % terms['slot_minutes']:
        return 'not_on_slot_grid'
    if Fraction(record['party_size']) > sum(Fraction(terms['capacities'][x]) for x in members(restaurant, record)):
        return 'party_exceeds_capacity'
    return None


def amend(restaurant, publications, before, patch, now):
    """Pure merged-record transition; caller separately checks collective occupancy."""
    expected = patch.get('expected_revision')
    if 'expected_revision' in patch:
        try:
            number = Fraction(expected) if not isinstance(expected, (bool, str, list, dict)) else None
        except (ValueError, TypeError, OverflowError):
            number = None
        if number is None or number.denominator != 1 or number < 1:
            return 'validation_failed', copy.deepcopy(before), []
        if expected != before['revision']:
            return 'stale_revision', copy.deepcopy(before), []
    if before['status'] != 'confirmed':
        return 'reservation_cancelled', copy.deepcopy(before), []
    cutoff = before['accepted_terms']['cancellation_cutoff_minutes'] * 60
    if now >= prior.instant_seconds(before['starts_at']) - cutoff:
        return 'cutoff_passed', copy.deepcopy(before), []
    candidate = copy.deepcopy(before)
    if 'table_id' in patch or 'table_ids' in patch:
        candidate.pop('table_id', None); candidate.pop('table_ids', None)
        candidate['table_ids'] = members(restaurant, patch)
        if len(candidate['table_ids']) == 1:
            candidate['table_id'] = candidate['table_ids'][0]
    for field in ('starts_at_local', 'party_size'):
        if field in patch:
            candidate[field] = patch[field]
    delta = changes(restaurant, before, candidate)
    if not delta:
        return None, copy.deepcopy(before), []
    terms = selected(restaurant, publications, candidate['starts_at_local'][:10])
    error = validate_result(restaurant, terms, candidate)
    if error:
        return error, copy.deepcopy(before), []
    start = prior.resolve(candidate['starts_at_local'], restaurant['timezone'])
    end = (start.astimezone(dt.timezone.utc) + dt.timedelta(minutes=terms['reservation_duration_minutes'])).astimezone(ZoneInfo(restaurant['timezone']))
    candidate.update(revision=before['revision'] + 1, accepted_terms=terms,
                     starts_at=start.isoformat(), ends_at=end.isoformat())
    return None, candidate, delta


def counters(changed, memberships):
    """Only explicit Stage 3 collective deltas; no invented general-write rules."""
    actual = set(changed)
    return {'restaurant': int(bool(actual)),
            'reservations': {ref: 1 for ref in actual},
            'series': {sid: 1 for ref, sid in memberships.items() if ref in actual}}


def serial_outcomes(initial, operations, transition):
    outcomes = []
    for ordering in permutations(range(len(operations))):
        state = copy.deepcopy(initial); responses = {}
        for index in ordering:
            state, responses[index] = transition(state, operations[index])
        outcomes.append((state, responses))
    return outcomes


def calibrate():
    """Controlled wrong observations must fail independent reference comparisons."""
    r = fixture()['restaurants'][0]
    p1 = dict(policy(r, '2080-06-01'), policy_version=1)
    p2 = dict(policy(r, '2080-05-01', reservation_duration_minutes=120), policy_version=2)
    p3 = dict(policy(r, '2080-06-01', reservation_duration_minutes=60), policy_version=3)
    checks = []
    def detect(name, expected, wrong):
        assert expected != wrong, 'VERIFIER COVERAGE GAP: ' + name
        checks.append(name)
    detect('publication-order-instead-of-effective-date', selected(r, [p1, p2], '2080-06-06')['policy_version'], 2)
    detect('old-version-wins-effective-date-tie', selected(r, [p1, p2, p3], '2080-06-06')['policy_version'], 1)
    detect('future-policy-selected-early', selected(r, [p1], '2080-05-31')['policy_version'], 1)
    pair = {'table_ids': ['z', 'a'], 'starts_at_local': '2080-06-06T18:00', 'party_size': 6}
    normalized = dict(pair, table_ids=['a', 'z'])
    detect('reversed-pair-becomes-change', changes(r, pair, normalized), [{'field': 'table_ids'}])
    detect('pair-created-history-uses-single-field', changes(r, None, pair)[0]['field'], 'table_id')
    detect('pair-history-preserves-request-order', changes(r, None, pair)[0]['to'], ['z', 'a'])
    detect('history-records-unknown-field', changes(r, normalized, dict(normalized, ignored=1)), [{'field': 'ignored'}])
    detect('partial-terms-only-selected-capacities', set(baseline(r)['capacities']), {'a', 'z'})
    for zone, start, count in [('Europe/Berlin', '2026-10-18T02:30', 2), ('America/New_York', '2026-10-25T01:30', 2)]:
        local = local_occurrences(start, count, 1)[1]
        resolved = prior.resolve(local, zone)
        assert resolved is not None
        wrong = resolved.replace(fold=1)
        detect('second-fold-' + zone, prior.instant_seconds(resolved.isoformat()), prior.instant_seconds(wrong.isoformat()))
        anchor = prior.resolve(start, zone).astimezone(dt.timezone.utc)
        wrong_local = (anchor + dt.timedelta(days=7)).astimezone(ZoneInfo(zone)).isoformat(timespec='minutes')[:16]
        # At the repeated first occurrence, weekly UTC arithmetic can coincide.
        later = local_occurrences(start, 3, 1)[2]
        wrong_later = (anchor + dt.timedelta(days=14)).astimezone(ZoneInfo(zone)).isoformat(timespec='minutes')[:16]
        detect('utc-week-drift-' + zone, later, wrong_later)
    for zone, local in [('Europe/Berlin', '2027-03-28T02:30'), ('America/New_York', '2027-03-14T02:30')]:
        detect('gap-normalized-' + zone, prior.resolve(local, zone), local)
    detect('batch-counter-per-item', counters(['a', 'b'], {'a': 's', 'b': 's'})['series'], {'s': 2})
    detect('all-noop-counter-increment', counters([], {'a': 's'})['restaurant'], 1)
    detect('unchanged-only-series-increment', counters(['a'], {'a': 's', 'b': 't'})['series'], {'s': 1, 't': 1})
    start = prior.resolve('2080-06-06T18:00', r['timezone'])
    before = dict(normalized, status='confirmed', revision=1, starts_at=start.isoformat(),
                  ends_at=(start + dt.timedelta(minutes=90)).isoformat(), accepted_terms=baseline(r))
    restrictive = dict(policy(r, '2080-06-01', capacities={t['id']: 1 for t in r['tables']}), policy_version=1)
    error, unchanged, delta = amend(r, [restrictive], before, {'table_ids': ['z', 'a']}, 0)
    assert error is None and unchanged == before and delta == []
    detect('noop-replaces-accepted-terms', unchanged['accepted_terms'], selected(r, [restrictive], '2080-06-06'))
    error, unchanged, delta = amend(r, [], before, {'expected_revision': 2, 'party_size': 999}, 10**15)
    detect('cutoff-before-stale', error, 'cutoff_passed')
    error, unchanged, delta = amend(r, [restrictive], before, {'starts_at_local': '2080-06-06T18:30'}, 0)
    detect('real-change-skips-unmodified-party-validation', error, None)
    return {'status': 'PASS', 'controlled_faults_detected': len(checks), 'faults': checks,
            'scope': 'reference-model calibration only; no candidate execution'}
