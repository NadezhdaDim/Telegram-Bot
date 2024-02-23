import requests
import json
import re
from config import keys

class APIException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

       if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

       try:
            quote_ticker = keys[quote]
       except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

       try:
            base_ticker = keys[base]
       except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')


       r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
       total_base = json.loads(r.content)[keys[base]]

       if amount[0]=='-':
            raise APIException(f'Не удалось обработать количество {amount}.Введите значение больше 0')
       elif not re.match('^[0-9,.]+$', amount):
            raise APIException(f'Не удалось обработать количество {amount}. Введите число состоящее из цифр')
       else:
            amount = float(amount.replace(',','.'))
            total_base_sum = round(total_base*amount,2)

       return total_base_sum