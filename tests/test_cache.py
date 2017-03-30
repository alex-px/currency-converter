import json
import os
from converter.currency_converter import CACHE_FILE, _get_rates_usd


class TestCache:

    def test_cached(self):
        rates = {"GGP": 0.805647, "UGX": 3601.999708, "MGA": 3185.000239}
        with open(CACHE_FILE, 'w') as fh:
            json.dump(rates, fh)
        assert _get_rates_usd() == rates
        os.remove(CACHE_FILE)
