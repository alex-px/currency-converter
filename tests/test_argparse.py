import pytest
from converter.currency_converter import _get_args


class TestArgparse:

    def test_amount_required(self):
        with pytest.raises(SystemExit):
            _get_args().parse_args(['100.9', '-i', 'JPY'])

    def test_amount_short(self):
        result = _get_args().parse_args(['-a', '100.9', '-i', 'JPY'])
        assert result.amount == 100.9

    def test_amount_long(self):
        result = _get_args().parse_args(['-i', 'GBP', '--amount', '0.8'])
        assert result.amount == 0.8

    def test_amount_int(self):
        result = _get_args().parse_args(['-a', '4', '-i', 'JPY'])
        assert result.amount == 4

    def test_amount_numeric(self):
        with pytest.raises(SystemExit):
            _get_args().parse_args(['-a', 'not_valid', '-i', 'JPY'])

    def test_input_required(self):
        with pytest.raises(SystemExit):
            _get_args().parse_args(['GBP', '--amount', '0.8'])

    def test_input_short(self):
        result = _get_args().parse_args(['-i', 'GBP', '--amount', '0.8'])
        assert result.input_currency == "GBP"

    def test_input_long(self):
        result = _get_args().parse_args(['--input_currency', '₮', '--amount', '0.8'])
        assert result.input_currency == "₮"

    def test_output_short(self):
        result = _get_args().parse_args(['-i', 'CAD', '--amount', '0.8', '-o', 'CZK'])
        assert result.output_currency == "CZK"

    def test_output_long(self):
        result = _get_args().parse_args(['-i', 'CAD', '--amount', '0.8', '--output_currency', '₦'])
        assert result.output_currency == "₦"

    def test_output_empty(self):
        result = _get_args().parse_args(['-i', 'CAD', '--amount', '0.8'])
        assert result.output_currency is None
