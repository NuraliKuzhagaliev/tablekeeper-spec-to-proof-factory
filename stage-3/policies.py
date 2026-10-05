"""Immutable date-effective policy snapshots, separate from fixture identity."""
import copy
import re

from domain import APIError, WEEKDAYS, booking, fail, field, local_date, local_datetime, positive_integer

RULE_FIELDS = ('slot_minutes', 'reservation_duration_minutes', 'cancellation_cutoff_minutes', 'opening_hours')


def opening_hours(value):
    if type(value) is not list:
        fail('malformed_request', 400)
    result, seen = [], set()
    for entry in value:
        if type(entry) is not dict:
            fail('malformed_request', 400)
        hours = {key: field(entry, key, str) for key in ('weekday', 'opens', 'closes')}
        if hours['weekday'] not in WEEKDAYS or hours['weekday'] in seen:
            fail()
        seen.add(hours['weekday'])
        if any(not re.fullmatch(r'(?:[01][0-9]|2[0-3]):[0-5][0-9]', hours[key]) for key in ('opens', 'closes')):
            fail()
        if hours['opens'] >= hours['closes']:
            fail()
        result.append(hours)
    return result


def fixture_terms(restaurant):
    return {'policy_version': 0, **{key: copy.deepcopy(restaurant[key]) for key in RULE_FIELDS},
            'capacities': {table['id']: table['capacity'] for table in restaurant['tables']}}


def terms(policy):
    return {key: copy.deepcopy(policy[key]) for key in ('policy_version', *RULE_FIELDS, 'capacities')}


def complete_policy(restaurant, body):
    # The publication endpoint specifies 422 for every invalid recognized field.
    # Transport parsing still rejects unparseable/nonobject JSON with 400.
    try:
        effective = field(body, 'effective_from', str)
        local_date(effective)
        result = {'effective_from': effective}
        for name, minimum, maximum in (('slot_minutes', 1, 1440),
                                       ('reservation_duration_minutes', 1, 1440),
                                       ('cancellation_cutoff_minutes', 0, 10080)):
            value = positive_integer(body.get(name), zero=minimum == 0)
            if value > maximum:
                fail()
            result[name] = value
        result['opening_hours'] = opening_hours(field(body, 'opening_hours', list))
        capacities = field(body, 'capacities', dict)
        if set(capacities) != {table['id'] for table in restaurant['tables']}:
            fail()
        result['capacities'] = {}
        for table in restaurant['tables']:
            value = positive_integer(capacities[table['id']])
            if value > 100:
                fail()
            result['capacities'][table['id']] = value
        return result
    except (APIError, ValueError, TypeError, KeyError):
        fail()


def applicable_terms(state, restaurant, day):
    eligible = [policy for policy in state['policies'][restaurant['id']] if policy['effective_from'] <= day]
    if not eligible:
        return fixture_terms(restaurant)
    return terms(max(eligible, key=lambda policy: (policy['effective_from'], policy['policy_version'])))


def rules_config(restaurant, accepted):
    return {**restaurant, **{key: accepted[key] for key in RULE_FIELDS},
            'tables': [{**table, 'capacity': accepted['capacities'][table['id']]} for table in restaurant['tables']]}


def decided_booking(state, restaurant, body):
    local = local_datetime(field(body, 'starts_at_local', str))
    accepted = applicable_terms(state, restaurant, local.date().isoformat())
    return {**booking(rules_config(restaurant, accepted), body), 'accepted_terms': accepted}
