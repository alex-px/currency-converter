# currency-converter

Currency converter that uses www.apilayer.net as source.


Please note that cross rates are calculaded based on USD rates.

### Example 1:
> ./converter/currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK
```json
{   
    "input": {
        "amount": 100.0,
        "currency": "EUR"
    },
    "output": {
        "CZK": 2707.36, 
    }
}
```
### Example 2:
> ./converter/currency_converter.py --amount 10.92 --input_currency £ 
```json
{
    "input": {
        "amount": 10.92,
        "currency": "GBP"
    },
    "output": {
        "EUR": 14.95,
        "USD": 17.05,
        "CZK": 404.82,
        .
        .
        .
    }
}
```
