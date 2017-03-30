import os
import json
from converter.currency_converter import CACHE_FILE, convert_currency


class TestEndToEnd:

    def test_e2e_codes(self):
        rates = {"GGP": 0.805647, "UGX": 3601.999708, "GBP": 3185.000239}
        with open(CACHE_FILE, 'w') as fh:
            json.dump(rates, fh)
        result = convert_currency(10, 'GBP', 'UGX')
        assert json.loads(result) == {
            "input": {
                "amount": 10,
                "currency": "GBP"
            },
            "output": {
                "UGX": 11.31
            }
        }
        os.remove(CACHE_FILE)

    def test_e2e_symbols(self):
        rates = {"GGP": 0.805647, "UGX": 3601.999708, "GBP": 3185.000239}
        with open(CACHE_FILE, 'w') as fh:
            json.dump(rates, fh)
        result = convert_currency(10, '£', 'UGX')
        assert json.loads(result) == {
            "input": {
                "amount": 10,
                "currency": "GBP"
            },
            "output": {
                "UGX": 11.31
            }
        }
        os.remove(CACHE_FILE)

    def test_e2e_all_available(self):
        rates = {"GGP": 0.805647, "UGX": 3601.999708, "GBP": 1.000239, "RUB": 44.976}
        with open(CACHE_FILE, 'w') as fh:
            json.dump(rates, fh)
        result = convert_currency(10, '£')
        assert json.loads(result) == {
            "input": {
                "amount": 10,
                "currency": "GBP"
            },
            "output": {
                'GBP': 10.0,
                'GGP': 8.05,
                'RUB': 449.65,
                'UGX': 36011.39
            }
        }
        os.remove(CACHE_FILE)
