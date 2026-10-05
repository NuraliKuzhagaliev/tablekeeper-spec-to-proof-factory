"""Native immutable events and honest prior-stage known-state baselines."""
import copy
from datetime import datetime

from domain import UTC, members, read_timestamp, same_json, timestamp


def public(reservation):
    return {key: value for key, value in reservation.items() if key != 'user_id'}


def changes(before, after):
    result = []
    old_members = members(before) if before else None
    new_members = members(after)
    if old_members != new_members:
        pair = len(new_members) == 2 or (old_members is not None and len(old_members) == 2)
        result.append({'field': 'table_ids' if pair else 'table_id',
                       'from': old_members if pair else old_members[0] if old_members else None,
                       'to': list(new_members) if pair else new_members[0]})
    for name in ('starts_at_local', 'party_size'):
        if before is None or not same_json(before[name], after[name]):
            result.append({'field': name, 'from': before[name] if before else None, 'to': after[name]})
    return copy.deepcopy(result)


def entry(history, restaurant, before, after, event, plan_id=None):
    now = datetime.now(UTC)
    if history['entries']:
        now = max(now, read_timestamp(history['entries'][-1]['at']))
    result = {'seq': len(history['entries']) + 1, 'at': timestamp(now, restaurant['timezone']), 'event': event,
            'changes': [] if event == 'cancelled' else changes(before, after),
            'revision': after['revision'], 'accepted_terms': copy.deepcopy(after['accepted_terms'])}
    if event == 'reassigned':
        result['changes'] = [{'field': 'table_ids', 'from': list(members(before)), 'to': list(members(after))}]
        result['plan_id'] = plan_id
    return result


def native_history(restaurant, reservation):
    history = {'entries': [], 'provenance': {'kind': 'native'}}
    history['entries'].append(entry(history, restaurant, None, reservation, 'created'))
    return history


def baseline_history(reservation, kind='legacy_baseline'):
    # No event or time is invented for edits that older implementations did not
    # retain. Future native entries start at seq1 and carry their actual revisions.
    return {'entries': [], 'provenance': {'kind': kind, 'known_state': copy.deepcopy(public(reservation))}}
