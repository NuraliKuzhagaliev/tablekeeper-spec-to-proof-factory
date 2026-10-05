import unittest
from decimal import Decimal, localcontext
from itertools import product

from json_value import add_numbers, dumps, loads
from domain import same_json


class JSONValueTests(unittest.TestCase):
    def test_capacity_sums_preserve_units_and_compact_equal_exponents(self):
        with localcontext() as context:
            context.prec = 1000
            for left, right in [('1e309', '4'), ('9007199254740993.0', '7'), ('1e309', '2e309')]:
                actual = add_numbers(loads(left), loads(right))
                self.assertEqual(Decimal(dumps(actual)), Decimal(left) + Decimal(right))
        actual = add_numbers(loads('1e9999999999999999999999999'), loads('2e9999999999999999999999999'))
        self.assertTrue(same_json(actual, loads('3e9999999999999999999999999')))
        self.assertLess(len(dumps(actual)), 30)

    def test_exact_ordering_against_independent_decimal_oracle(self):
        tokens = ['0.0', '-0.0', '1.0', '-1.0', '0.001', '-0.001', '10.0', '-10.0',
                  '1e309', '-1e309', '1e-400', '-1e-400', '0.0100', '9007199254740993.0']
        for left, right in product(tokens, repeat=2):
            a, b = loads(left), loads(right)
            self.assertEqual(a == b, Decimal(left) == Decimal(right), (left, right))
            self.assertEqual(a < b, Decimal(left) < Decimal(right), (left, right))

    def test_json_number_equality_and_lossless_round_trip(self):
        groups = [['1e309', '10e308', '1.00e309'], ['1e-400', '0.1e-399', '10e-401'],
                  ['9007199254740993.0', '9007199254740993'], ['-0.0', '0e1000000000000000000000000', '0'],
                  ['1e9999999999999999999999999', '10e9999999999999999999999998']]
        for group in groups:
            values = [loads(token) for token in group]
            self.assertTrue(all(same_json(values[0], value) for value in values))
            for value in values:
                self.assertTrue(same_json(value, loads(dumps(value))))
        self.assertFalse(same_json(loads('1.0'), True))
        self.assertFalse(same_json(loads('1e-400'), 0))
        self.assertFalse(same_json(loads('9007199254740993.0'), loads('9007199254740992.0')))

    def test_non_json_constants_still_fail(self):
        for constant in ['NaN', 'Infinity', '-Infinity']:
            with self.assertRaises(ValueError):
                loads('{"ignored":' + constant + '}')
