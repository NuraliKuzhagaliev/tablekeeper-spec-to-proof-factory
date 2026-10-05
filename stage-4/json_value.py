"""Lossless JSON numbers, including exponents outside machine numeric ranges.

JSON specifies decimal numeric syntax, not an IEEE-754 magnitude or precision
limit. Retain exponent-form tokens without expanding them. A normalized decimal
coefficient/exponent supports exact value equality, integer validation and ordering.
The same codec writes snapshots and responses, so receipts remain portable.
"""
import functools
import json
import math
import sys

# Python's decimal-to-int text guard is not part of the HTTP JSON contract.
# Exponents stay compact; no power-of-ten expansion is needed for comparison.
sys.set_int_max_str_digits(0)


def is_number(value):
    return type(value) in (int, float, JSONNumber)


@functools.total_ordering
class JSONNumber:
    def __init__(self, token):
        self.token = token
        significand, separator, exponent = token.lower().partition('e')
        self.negative = significand.startswith('-')
        significand = significand.lstrip('-')
        whole, point, fraction = significand.partition('.')
        digits = (whole + fraction).lstrip('0')
        scale = (int(exponent) if separator else 0) - len(fraction)
        if not digits:
            self.negative, self.digits, self.scale = False, '0', 0
        else:
            trimmed = digits.rstrip('0')
            self.digits, self.scale = trimmed, scale + len(digits) - len(trimmed)

    @property
    def is_integer(self):
        return self.scale >= 0

    def model_integer(self):
        # Ordinary model values stay plain ints. Large values remain compact;
        # even a valid number such as 1e1000000000 never allocates a billion digits.
        if not self.is_integer:
            raise ValueError('fractional number')
        if len(self.digits) + self.scale <= 19:
            magnitude = int(self.digits) * 10 ** self.scale
            return -magnitude if self.negative else magnitude
        return self

    def bounded_integer(self):
        result = self.model_integer()
        if type(result) is not int:
            raise ValueError('integer outside bounded operation')
        return result

    def __int__(self):
        return self.bounded_integer()

    @staticmethod
    def from_value(value):
        if type(value) is JSONNumber:
            return value
        if type(value) is int:
            return JSONNumber(str(value))
        if type(value) is float and math.isfinite(value):
            return JSONNumber(str(value))
        raise ValueError('not a JSON number')

    def __eq__(self, other):
        if not is_number(other):
            return NotImplemented
        other = self.from_value(other)
        return (self.negative, self.digits, self.scale) == (other.negative, other.digits, other.scale)

    def __lt__(self, other):
        if not is_number(other):
            return NotImplemented
        other = self.from_value(other)
        if self.negative != other.negative:
            return self.negative
        if self.digits == '0' or other.digits == '0':
            smaller = self.digits == '0' and other.digits != '0'
        else:
            width, other_width = len(self.digits) + self.scale, len(other.digits) + other.scale
            if width != other_width:
                smaller = width < other_width
            else:
                length = max(len(self.digits), len(other.digits))
                smaller = self.digits.ljust(length, '0') < other.digits.ljust(length, '0')
        return other != self and (not smaller if self.negative else smaller)


def reject_constant(token):
    raise ValueError('non-JSON numeric constant')


def loads(value):
    return json.loads(value, parse_float=JSONNumber, parse_constant=reject_constant)


def add_numbers(left, right):
    """Exact addition for summed table capacities, without binary floats."""
    if type(left) is int and type(right) is int:
        return left + right
    a, b = JSONNumber.from_value(left), JSONNumber.from_value(right)
    if a.digits == '0':
        return b.model_integer() if b.is_integer else b
    if b.digits == '0':
        return a.model_integer() if a.is_integer else a
    scale = min(a.scale, b.scale)
    a_coefficient = int(a.digits + '0' * (a.scale - scale))
    b_coefficient = int(b.digits + '0' * (b.scale - scale))
    if a.negative:
        a_coefficient = -a_coefficient
    if b.negative:
        b_coefficient = -b_coefficient
    return JSONNumber(str(a_coefficient + b_coefficient) + 'e' + str(scale)).model_integer()


def dumps(value):
    if type(value) is JSONNumber:
        return value.token
    if type(value) is dict:
        return '{' + ','.join(json.dumps(key, ensure_ascii=True) + ':' + dumps(item) for key, item in value.items()) + '}'
    if type(value) is list or type(value) is tuple:
        return '[' + ','.join(dumps(item) for item in value) + ']'
    return json.dumps(value, ensure_ascii=True, separators=(',', ':'), allow_nan=False)
