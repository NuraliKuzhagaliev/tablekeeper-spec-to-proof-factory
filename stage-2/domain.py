"""Validation and timezone rules shared by writes, fixtures and snapshots."""
import hashlib
import hmac
import re
import secrets
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from json_value import JSONNumber, is_number

UTC = timezone.utc
WEEKDAYS = ('mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun')


class APIError(Exception):
    def __init__(self, status, code):
        self.status, self.code = status, code
        super().__init__(code.replace('_', ' '))


def fail(code='validation_failed', status=422):
    raise APIError(status, code)


def field(body, name, kind, required=True):
    if name not in body:
        if required:
            fail()
        return None
    value = body[name]
    if type(value) is not kind and not (kind is int and is_number(value)):
        fail('malformed_request', 400)
    return value


def identifier(value):
    if not isinstance(value, str) or not 1 <= len(value) <= 64:
        fail()
    return value


def party(value):
    # JSON numbers have no integer/float distinction; booleans are not numbers.
    if not is_number(value):
        fail()
    try:
        number = JSONNumber.from_value(value)
    except ValueError:
        fail()
    if not number.is_integer or number < 1:
        fail()
    return number.model_integer()


def positive_integer(value, zero=False):
    if not is_number(value):
        fail()
    try:
        number = JSONNumber.from_value(value)
    except ValueError:
        fail()
    if not number.is_integer or number < (0 if zero else 1):
        fail()
    return number.model_integer()


def local_datetime(value):
    if not isinstance(value, str):
        fail('malformed_request', 400)
    if not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}', value):
        fail()
    try:
        return datetime.strptime(value, '%Y-%m-%dT%H:%M')
    except ValueError:
        fail()


def local_date(value):
    if not re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}', value):
        fail()
    try:
        return datetime.strptime(value, '%Y-%m-%d').date()
    except ValueError:
        fail()


def fixed_instant(local, zone):
    # Fixed-offset datetimes preserve absolute comparison/addition semantics.
    # They can also describe valid local dates whose UTC equivalent is outside
    # datetime's year range; converting every instant to a UTC datetime cannot.
    aware = local.replace(tzinfo=ZoneInfo(zone), fold=0)
    return aware.replace(tzinfo=timezone(aware.utcoffset()))


def in_zone(instant, zone):
    target = ZoneInfo(zone)
    try:
        return instant.astimezone(target)
    except OverflowError:
        # UTC conversion may cross year 0/10000 while the resulting local date
        # remains valid. A Gregorian 400-year cycle preserves month/day/weekday.
        # At the upper boundary IANA future rules repeat on that cycle; at the
        # lower boundary the pre-transition offset is constant. Use a safe
        # surrogate only for the otherwise unrepresentable intermediate UTC date.
        shift = -400 if instant.year > 5000 else 400
        surrogate = instant.replace(year=instant.year + shift).astimezone(target)
        return surrogate.replace(year=surrogate.year - shift)


def resolve(local, zone):
    # fold=0 always selects the first occurrence of a repeated local time.
    absolute = fixed_instant(local, zone)
    if in_zone(absolute, zone).replace(tzinfo=None) != local:
        fail('invalid_local_time')
    return absolute


def timestamp(absolute, zone='UTC'):
    return in_zone(absolute, zone).isoformat(timespec='seconds')


def read_timestamp(value):
    if not isinstance(value, str):
        fail()
    try:
        result = datetime.fromisoformat(value)
        if result.tzinfo is None:
            fail()
        return result
    except (ValueError, OverflowError):
        fail()


def bounds(restaurant, day):
    hours = next((h for h in restaurant['opening_hours'] if h['weekday'] == WEEKDAYS[day.weekday()]), None)
    if hours is None:
        return None
    opening = datetime.combine(day, datetime.strptime(hours['opens'], '%H:%M').time())
    closing = datetime.combine(day, datetime.strptime(hours['closes'], '%H:%M').time())
    return opening, closing


def booking(restaurant, body):
    table_id = identifier(field(body, 'table_id', str))
    table = next((t for t in restaurant['tables'] if t['id'] == table_id), None)
    if table is None:
        fail('not_found', 404)
    if 'party_size' not in body:
        fail()
    count = party(body['party_size'])
    local = local_datetime(field(body, 'starts_at_local', str))
    start = resolve(local, restaurant['timezone'])
    hours = bounds(restaurant, local.date())
    if hours is None or local < hours[0] or local >= hours[1]:
        fail('outside_opening_hours')
    # Fixed offsets make durations and comparisons absolute across DST changes.
    closing = fixed_instant(hours[1], restaurant['timezone'])
    if restaurant['reservation_duration_minutes'] > (closing - start).total_seconds() / 60:
        fail('outside_opening_hours')
    end = start + timedelta(minutes=int(restaurant['reservation_duration_minutes']))
    elapsed = int((local - hours[0]).total_seconds() // 60)
    grid = restaurant['slot_minutes']
    if elapsed and (grid > elapsed or elapsed % int(grid)):
        fail('not_on_slot_grid')
    if count > table['capacity']:
        fail('party_exceeds_capacity')
    return {'restaurant_id': restaurant['id'], 'table_id': table_id, 'party_size': count,
            'starts_at_local': local.isoformat(timespec='minutes'),
            'starts_at': timestamp(start, restaurant['timezone']),
            'ends_at': timestamp(end, restaurant['timezone'])}


def overlaps(a, b):
    return (a['status'] == b['status'] == 'confirmed' and a['restaurant_id'] == b['restaurant_id']
            and a['table_id'] == b['table_id'] and read_timestamp(a['starts_at']) < read_timestamp(b['ends_at'])
            and read_timestamp(b['starts_at']) < read_timestamp(a['ends_at']))


def hash_password(password):
    salt = secrets.token_hex(16)
    digest = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=16384, r=8, p=1).hex()
    return {'algorithm': 'scrypt', 'salt': salt, 'digest': digest}


def valid_hash(value):
    return (type(value) is dict and value.get('algorithm') == 'scrypt'
            and isinstance(value.get('salt'), str) and re.fullmatch('[0-9a-f]{32}', value['salt'])
            and isinstance(value.get('digest'), str) and re.fullmatch('[0-9a-f]{128}', value['digest']))


def check_password(password, stored):
    digest = hashlib.scrypt(password.encode(), salt=bytes.fromhex(stored['salt']), n=16384, r=8, p=1).hex()
    return hmac.compare_digest(digest, stored['digest'])


def email(value):
    if not re.fullmatch(r'[^\s@]+@[^\s@]+', value):
        fail()
    return value


def same_json(a, b):
    if type(a) is bool or type(b) is bool:
        return type(a) is type(b) and a == b
    if is_number(a) and is_number(b):
        return JSONNumber.from_value(a) == JSONNumber.from_value(b)
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return a.keys() == b.keys() and all(same_json(a[k], b[k]) for k in a)
    if isinstance(a, list):
        return len(a) == len(b) and all(same_json(x, y) for x, y in zip(a, b))
    return a == b
