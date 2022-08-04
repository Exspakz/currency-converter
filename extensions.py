import requests
import json
from config import keys


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(vals):

        if len(vals) != 3:
            raise APIException('Неверное количество параметров, должно быть 3(три)')

        quote, base, amount = vals

        if quote == base:
            raise APIException(f'Невозможно конвертировать одинаковые валюты - {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту - {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту - {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество - {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/'
                         f'price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        text = f'Цена {int(amount)} {quote} в {base} - {round((total_base * float(amount)), 2)}'

        return text
