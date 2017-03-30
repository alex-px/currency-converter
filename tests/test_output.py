import json
from converter.currency_converter import _generate_output_json


class TestOutput:
    def test_output_multi(self):
        result = _generate_output_json(3.3, 'EUR', {"RUB": 45.54323, "CZK": 94.98393})
        assert json.loads(result) == {
            "input": {
                "amount": 3.3,
                "currency": "EUR"
            },
            "output": {
                "RUB": 45.54,
                "CZK": 94.98
            }
        }

    def test_output_single(self):
        result = _generate_output_json(10, 'GBP', {"RUB": 45.54923})
        assert json.loads(result) == {
            "input": {
                "amount": 10,
                "currency": "GBP"
            },
            "output": {
                "RUB": 45.55
            }
        }
