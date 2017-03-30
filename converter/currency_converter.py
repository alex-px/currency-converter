import argparse
import json
from datetime import datetime, timedelta
from os import path
from collections import OrderedDict
import requests
from currencies import currency_codes


CACHE_FILE = 'cache.json'
CACHE_TTL_IN_SECONDS = 360
API_URL = 'http://www.apilayer.net/api/live'
API_KEY = 'b83b78f27b96fac2c4e2a024040fd131'


class CustomRequestError(Exception):
    """Just to raise this custom error in case of failure during request or parsing response from API."""
    pass


def _get_args():
    """Returns ArgumentParser instance with parsed arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--amount', required=True, type=float, help='Amount for conversion')
    parser.add_argument('-i', '--input_currency', choices=currency_codes, required=True, help='Currency to convert from')
    parser.add_argument('-o', '--output_currency', choices=currency_codes, help='Currency to convert to. Can be omitted')

    return parser


def _make_rates_request():
    """Makes request to specified API and parses response"""
    r = requests.get('{0}?access_key={1}'.format(API_URL, API_KEY))
    try:
        r.raise_for_status()
    except:
        raise CustomRequestError('Something went wrong during request to API.')

    if r.status_code == 200 and r.json()['success']:
        # as we receive USDXXX rates we should truncate first three chars
        return {k[3:]: v for k, v in r.json()['quotes'].items()}
    else:
        raise CustomRequestError('Unable to parse response.')


def _get_rates_usd():
    """Returns dict with rates from cached file or makes API call and updates cache"""
    try:
        modified_at = path.getmtime(CACHE_FILE)
    except OSError:
        modified_at = 0

    # cache still valid
    if datetime.now() - datetime.fromtimestamp(modified_at) < timedelta(seconds=CACHE_TTL_IN_SECONDS):
        with open(CACHE_FILE, 'r') as fh:
            return json.load(fh)

    # make request and update cache
    rates_dict = _make_rates_request()
    with open(CACHE_FILE, 'w') as fh:
        json.dump(rates_dict, fh)
    return rates_dict


def _generate_output_json(amount, input_curr, cross_rates):
    """Generates and returns string in JSON format with requested data"""
    input_values = OrderedDict()
    input_values['amount'] = amount
    input_values['currency'] = input_curr

    result = OrderedDict()
    result['input'] = input_values
    result['output'] = {k: round(v, 2) for k, v in cross_rates.items()}
    return json.dumps(result, indent=4)


def convert_currency(amount, input_curr, output_curr=None):
    """
    Converts given amount of input currency to specified currency or to all available currencies using USD cross-rates
    :param amount: amount to convert
    :param input_curr: input currency code or symbol
    :param output_curr: output currency code or symbol. Can be omitted.
    :return: String in JSON format
    """
    assert isinstance(amount, (float, int)), 'Input amount should be a number.'
    rates = _get_rates_usd()
    try:
        input_code = currency_codes[input_curr]
        input_value = rates[input_code]
    except KeyError:
        raise KeyError('Could not find rate for given input currency: "{}"'.format(input_curr))

    if output_curr:
        try:
            output_code = currency_codes[output_curr]
            output_value = rates[output_code]
        except KeyError:
            raise KeyError('Could not find rate for given output currency: "{}"'.format(output_curr))
        cross_rates = {output_code: output_value / input_value * amount}
    else:
        cross_rates = {currency: rate/input_value*amount for currency, rate in rates.items()}

    return _generate_output_json(amount, input_code, cross_rates)


if __name__ == '__main__':
    args = _get_args().parse_args()
    print(convert_currency(args.amount, args.input_currency, args.output_currency))
