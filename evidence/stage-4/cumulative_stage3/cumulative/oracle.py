"""Independent Stage 2 reference calculations; never imports production modules."""
import copy
import datetime as dt
from decimal import Decimal, localcontext
from fractions import Fraction
from itertools import combinations
from zoneinfo import ZoneInfo
import stage1_campaign as prior

check = prior.check
DAY = prior.DAY


def fixture(**kwargs):
    fx = prior.fixture(**kwargs)
    r = fx['restaurants'][0]
    r['name'] = 'The Lantern Courtyard'
    r['tables'] = [{'id': 'z', 'label': 'Window alcove', 'capacity': 4},
                   {'id': 'a', 'label': 'Courtyard bench', 'capacity': 2},
                   {'id': 'm', 'label': 'Chef’s nook', 'capacity': 6},
                   {'id': 'q', 'label': 'Terrace corner', 'capacity': 2}]
    r['combinable'] = [['a', 'z'], ['m', 'q'], ['z', 'm']]
    return fx


def members(record):
    if 'table_ids' in record:
        return tuple(record['table_ids'])
    return (record['table_id'],)


def current_shape(record):
    ids = record.get('table_ids')
    check(isinstance(ids, list) and 1 <= len(ids) <= 2
          and all(isinstance(x, str) for x in ids) and len(set(ids)) == len(ids),
          'current reservation lacks valid table_ids')
    if len(ids) == 1:
        check(record.get('table_id') == ids[0], 'single response selection mismatch')
    else:
        check('table_id' not in record, 'pair response carries table_id')


def audit(rows, current=True):
    check(isinstance(rows, list), 'reservation list not array')
    if current:
        for row in rows:
            current_shape(row)
    check(len({r['reference'] for r in rows}) == len(rows), 'duplicate references')
    check(len({r['reservation_id'] for r in rows}) == len(rows), 'duplicate reservation IDs')
    starts = [prior.instant_seconds(r['starts_at']) for r in rows]
    ends = [prior.instant_seconds(r['ends_at']) for r in rows]
    check(starts == sorted(starts, reverse=True), 'non-descending absolute starts')
    for i, r in enumerate(rows):
        check(r['status'] in ('confirmed', 'cancelled') and ends[i] > starts[i], 'invalid record interval/status')
        for j in range(i):
            other = rows[j]
            if (r['restaurant_id'] == other['restaurant_id'] and r['status'] == other['status'] == 'confirmed'
                    and set(members(r)) & set(members(other))):
                check(not prior.overlaps(starts[i], ends[i], starts[j], ends[j]), 'overlapping confirmed member')


def selections(restaurant):
    capacities = {t['id']: t['capacity'] for t in restaurant['tables']}
    result = [(tuple([t['id']]), t['capacity']) for t in restaurant['tables']]
    result += [(tuple(pair), sum(Fraction(capacities[x]) for x in pair)) for pair in restaurant.get('combinable', [])]
    return result


def allowed(restaurant, ids):
    return len(ids) == 1 or (len(ids) == 2 and any(set(ids) == set(p) for p in restaurant.get('combinable', [])))


def slots(fx, date, party, occupied=(), restaurant_id=None):
    r = next(x for x in fx['restaurants'] if restaurant_id is None or x['id'] == restaurant_id)
    hours = next((x for x in r['opening_hours'] if x['weekday'] == prior.WEEK[dt.date.fromisoformat(date).weekday()]), None)
    if hours is None:
        return []
    def minute(text):
        h, m = map(int, text.split(':'))
        return h * 60 + m
    close = prior.resolve(date + 'T' + hours['closes'], r['timezone'])
    check(close is not None, 'oracle fixture has unspecified gap-valued close')
    close_instant = prior.instant_seconds(close.isoformat())
    result = []
    # Bound minute enumeration before constructing any subsequent calendar date.
    for value in range(minute(hours['opens']), minute(hours['closes']), int(r['slot_minutes'])):
        local = f'{date}T{value // 60:02d}:{value % 60:02d}'
        start = prior.resolve(local, r['timezone'])
        if start is None:
            continue
        start_instant = prior.instant_seconds(start.isoformat())
        end_instant = start_instant + r['reservation_duration_minutes'] * 60
        if end_instant > close_instant:
            continue
        options = []
        for ids, capacity in selections(r):
            if capacity < party:
                continue
            taken = any(x['restaurant_id'] == r['id'] and x['status'] == 'confirmed'
                        and set(ids) & set(members(x))
                        and prior.overlaps(start_instant, end_instant,
                                           prior.instant_seconds(x['starts_at']), prior.instant_seconds(x['ends_at']))
                        for x in occupied)
            if not taken:
                options.append({'table_ids': list(ids), 'capacity': capacity})
        result.append({'starts_at_local': local, 'starts_at': start.isoformat(),
                       'available_table_ids': [x['table_ids'][0] for x in options if len(x['table_ids']) == 1],
                       'available_options': options})
    return result


def json_identity(value):
    """Typed parsed-JSON identity: numbers exact, arrays ordered, objects unordered."""
    if value is None:
        return ('null',)
    if isinstance(value, bool):
        return ('bool', value)
    if isinstance(value, (int, Decimal, float)):
        return ('number', Decimal(str(value)))
    if isinstance(value, str):
        return ('string', value)
    if isinstance(value, list):
        return ('array', tuple(json_identity(x) for x in value))
    if isinstance(value, dict):
        return ('object', tuple(sorted((k, json_identity(v)) for k, v in value.items())))
    raise TypeError('non-JSON verifier value')


def migrate_record_expectation(record):
    """Current-record extension only. Never apply this to a historical receipt."""
    result = copy.deepcopy(record)
    result['table_ids'] = list(members(record))
    return result


def feasible_capacity_vectors():
    """Finite test bounds, not a service numeric-range restriction.

    Rational arithmetic supplies the expected sum without binary64 or Decimal
    context rounding; compact input exponents can imply much larger output.
    """
    vectors = []
    for left, right in [('1e18', '1'), ('1e56', '1e29'), ('1e309', '2'),
                        ('1e1000', '1e7'), ('1e2048', '1e17')]:
        total = Fraction(Decimal(left)) + Fraction(Decimal(right))
        check(total.denominator == 1, 'capacity vector must have integer sum')
        vectors.append({'left': Decimal(left), 'right': Decimal(right),
                        'sum': total.numerator,
                        'exact_sum_decimal_digits': len(str(total.numerator))})
    return vectors


def calibrate():
    prior.calibrate()
    fx = fixture(zone='UTC')
    r = fx['restaurants'][0]
    check(allowed(r, ('z', 'a')) and not allowed(r, ('a', 'm')), 'approval transitivity mutant escaped')
    all_options = slots(fx, DAY, 1)[0]['available_options']
    check([x['table_ids'] for x in all_options] == [['z'], ['a'], ['m'], ['q'], ['a', 'z'], ['m', 'q'], ['z', 'm']],
          'order mutant escaped')
    record = {'reservation_id': 'one', 'reference': 'CAL001', 'restaurant_id': 'r', 'table_ids': ['a', 'z'],
              'status': 'confirmed', 'starts_at': DAY + 'T18:00:00+00:00', 'ends_at': DAY + 'T19:30:00+00:00'}
    options = slots(fx, DAY, 1, [record])[0]['available_options']
    check([x['table_ids'] for x in options] == [['m'], ['q'], ['m', 'q']], 'whole-set overlap mutant escaped')
    check(json_identity([1]) != json_identity([True]), 'bool/number mutant escaped')
    check(json_identity(['a', 'z']) != json_identity(['z', 'a']), 'pair-array normalization mutant escaped')
    check(json_identity({'v': Decimal('1e309')}) == json_identity({'v': Decimal('10e308')}), 'number equivalence')
    check(json_identity(Decimal('1.0000000000000000001')) != json_identity(Decimal('1.0')), 'precision collapse')
    giant = copy.deepcopy(r)
    giant['tables'][0]['capacity'] = Decimal('1e309')
    check(dict(selections(giant))[('a', 'z')] == Fraction(Decimal('1e309')) + 2,
          'independent summed capacity lost low-order integer')
    vectors = feasible_capacity_vectors()
    for vector in vectors:
        giant['tables'][0]['capacity'] = vector['left']
        giant['tables'][1]['capacity'] = vector['right']
        check(dict(selections(giant))[('a', 'z')] == vector['sum'], 'disparate-exponent exact sum')
        expected_token = str(vector['sum'])
        decoded = prior.encode_json(vector['sum'])
        check(decoded == expected_token, 'verifier integer serializer changed sum')
        # A deliberately low-precision addition represents a plausible rounded
        # implementation; the rational reference must distinguish it.
        with localcontext() as context:
            context.prec = 16
            check(Fraction(vector['left'] + vector['right']) != vector['sum'],
                  'rounded-sum calibration failed to detect low-order loss')
    # Bounded brute-force occupancy metamorphism over every single/approved pair.
    choices = selections(r)
    comparisons = 0
    for ids, _ in choices:
        occupied = [{**record, 'table_ids': list(ids)}]
        found = {tuple(x['table_ids']) for x in slots(fx, DAY, 1, occupied)[0]['available_options']}
        expected = {other for other, _ in choices if not set(ids) & set(other)}
        check(found == expected, 'exhaustive member exclusion mismatch')
        comparisons += len(choices)
    return {'calibration': 'PASS', 'additional_variants': ['transitive-approval', 'wrong-option-order',
            'whole-set-overlap', 'bool-number-collapse', 'pair-array-normalization', 'precision-collapse'],
            'bounded_member_comparisons': comparisons, 'feasible_exact_capacity_vectors': len(vectors),
            'maximum_exact_sum_decimal_digits': max(v['exact_sum_decimal_digits'] for v in vectors),
            'production_executed': False}
