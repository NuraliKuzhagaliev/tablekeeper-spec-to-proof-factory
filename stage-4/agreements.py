"""Immutable scheduled-date provenance and collective amendment controls."""
import re
import json

from domain import fail, local_date, positive_integer


def amendment_controls(body, count):
    expected = positive_integer(body.get('expected_revision'))
    start = positive_integer(body.get('from_index'), zero=True)
    clock = body.get('local_time')
    if start >= count or type(clock) is not str or not re.fullmatch(r'(?:[01][0-9]|2[0-3]):[0-5][0-9]', clock):
        fail()
    return expected, int(start), clock


def initialize_schedules(state, agreement):
    """Read only preserved adoption truth, never the current edited anchor."""
    originals = [receipt['response'] for scope, receipt in state['receipts'].items()
                 if json.loads(scope)[2] == '/series' and receipt['response'].get('series_id') == agreement['series_id']]
    if not originals:
        fail()
    original = originals[0]
    if len(original['occurrences']) != len(agreement['occurrences']):
        fail()
    for item in agreement['occurrences']:
        retained = original['occurrences'][int(item['index'])]
        if retained['reference'] != item['reference']:
            fail()
        expected = retained['reservation']['starts_at_local'][:10]
        if 'scheduled_date' in item and item['scheduled_date'] != expected:
            fail()
        item['scheduled_date'] = expected
        local_date(item['scheduled_date'])
