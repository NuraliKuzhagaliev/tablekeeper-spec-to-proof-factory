"""Pure exact seating optimization over immutable accepted booking intervals."""
import re

from domain import fail, field, identifier, members, overlaps, read_timestamp
from json_value import JSONNumber, add_numbers


def subtract(left, right):
    value = JSONNumber.from_value(right)
    negative = JSONNumber(('-' if not value.negative else '') + value.digits + 'e' + str(value.scale))
    return add_numbers(left, negative)


def closure_request(restaurant, body):
    table = identifier(field(body, 'table_id', str))
    if table not in {item['id'] for item in restaurant['tables']}:
        fail('not_found', 404)
    result = {'table_id': table}
    for name in ('from', 'to'):
        value = field(body, name, str)
        if not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\.[0-9]+)?(?:Z|[+-][0-9]{2}:[0-9]{2})', value):
            fail()
        # Keep supplied offset/fraction spelling and compare absolute instants.
        read_timestamp(value)
        result[name] = value
    if instant_key(result['from']) >= instant_key(result['to']):
        fail()
    return result


def closure_record(rid, closure):
    return {'restaurant_id': rid, 'status': 'confirmed', 'table_ids': [closure['table_id']],
            'starts_at': closure['from'], 'ends_at': closure['to']}


def closed(record, closures):
    return record['status'] == 'confirmed' and any(item['table_id'] in members(record)
            and interval_overlap(record, closure_record(record['restaurant_id'], item)) for item in closures)


def instant_key(value):
    # datetime validates calendar/offset syntax, while a decimal fractional part
    # retains precision beyond microseconds for closure ordering and overlap.
    instant = read_timestamp(value)
    seconds = instant.date().toordinal() * 86400 + instant.hour * 3600 + instant.minute * 60 + instant.second
    seconds -= int(instant.utcoffset().total_seconds())
    fraction = re.search(r'T[0-9]{2}:[0-9]{2}:[0-9]{2}\.([0-9]+)', value)
    return seconds, JSONNumber('0.' + fraction[1]) if fraction else 0


def interval_overlap(a, b):
    return instant_key(a['starts_at']) < instant_key(b['ends_at']) and instant_key(b['starts_at']) < instant_key(a['ends_at'])


def assigned(record, selection):
    result = {**record, 'table_ids': list(selection)}
    result.pop('table_id', None)
    if len(selection) == 1:
        result['table_id'] = selection[0]
    return result


def solve(restaurant, records, closures, proposed):
    """Return the full rank-vector optimum; do not mutate input or state.

    At most ten ranked options and six considered bookings. Precompute retained
    interval compatibility and fixed/closure exclusions. Branch lower bounds are
    independent per-booking minima, hence admissible even when they cannot all
    coexist. Exact decimal arithmetic is used for every objective and bound.
    """
    rid = restaurant['id']
    active = [record for record in records if record['restaurant_id'] == rid and record['status'] == 'confirmed']
    considered = sorted((record for record in active if interval_overlap(record, closure_record(rid, proposed))), key=lambda record: record['reference'])
    if len(restaurant['tables']) > 6 or len(restaurant['combinable']) > 4 or len(considered) > 6:
        fail('planning_limit')
    references = {record['reference'] for record in considered}
    fixed = [record for record in active if record['reference'] not in references]
    selections = [[table['id']] for table in restaurant['tables']] + restaurant['combinable']
    bits = {table['id']: 1 << index for index, table in enumerate(restaurant['tables'])}
    choices = []
    for record in considered:
        options = []
        for rank, selection in enumerate(selections):
            capacities = record['accepted_terms']['capacities']
            capacity = capacities[selection[0]]
            if len(selection) == 2:
                capacity = add_numbers(capacity, capacities[selection[1]])
            if capacity < record['party_size']:
                continue
            candidate = assigned(record, selection)
            if closed(candidate, [*closures, proposed]) or any(overlaps(candidate, other) for other in fixed):
                continue
            options.append({'rank': rank, 'selection': list(selection), 'mask': sum(bits[table] for table in selection),
                            'changed': set(selection) != set(members(record)), 'waste': subtract(capacity, record['party_size'])})
        if not options:
            fail('no_feasible_plan', 409)
        choices.append(sorted(options, key=lambda option: (option['changed'], option['waste'], option['rank'])))
    conflicts = [[interval_overlap(a, b) for b in considered] for a in considered]
    suffix_changes, suffix_waste, suffix_ranks = [0], [0], [()]
    for options in reversed(choices):
        suffix_changes.append(suffix_changes[-1] + min(option['changed'] for option in options))
        suffix_waste.append(add_numbers(suffix_waste[-1], min(option['waste'] for option in options)))
        suffix_ranks.append((min(option['rank'] for option in options),) + suffix_ranks[-1])
    suffix_changes.reverse(); suffix_waste.reverse(); suffix_ranks.reverse()
    best, winner = None, None

    def visit(index, selected, moved, waste, ranks):
        nonlocal best, winner
        lower = (moved + suffix_changes[index], add_numbers(waste, suffix_waste[index]), ranks + suffix_ranks[index])
        if best is not None and lower >= best:
            return
        if index == len(considered):
            best, winner = (moved, waste, ranks), list(selected)
            return
        for option in choices[index]:
            if any(conflicts[index][previous] and option['mask'] & old['mask'] for previous, old in enumerate(selected)):
                continue
            visit(index + 1, [*selected, option], moved + option['changed'], add_numbers(waste, option['waste']), ranks + (option['rank'],))

    visit(0, [], 0, 0, ())
    if winner is None:
        fail('no_feasible_plan', 409)
    return {'assignments': [{'reference': record['reference'], 'table_ids': option['selection'], 'changed': option['changed']}
                            for record, option in zip(considered, winner)], 'moved_count': best[0], 'unused_seats': best[1]}
