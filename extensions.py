import requests
import json
from config import keys

class APIException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if base == quote:
            raise APIException(f'Not possible to convert the same currency {base}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Currency {base} is not in the list. Check /values')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Currency {quote} is not in the list. Check /values')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Amount {amount} is not a number')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={base_ticker}&tsyms={quote_ticker}')
        total = json.loads(r.content)[quote_ticker]*amount
        return total