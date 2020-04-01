from django.core.management.base import BaseCommand
from currency.models import Rate
import requests
from datetime import timedelta, date
from currency import model_choices as mch


class Command(BaseCommand):

    def handle(self, *args, **options):

        HOST = 'https://api.privatbank.ua'
        ROOT_PATH = '/p24api/exchange_rates'

        d = date(2014, 11, 30)

        while d < date.today():

            d += timedelta(days=1)
            print(d)
            print(date.today())
            param = f'{d.day}.{d.month}.{d.year}'
            response = requests.get(HOST + ROOT_PATH + r'?json&date=' + f'{param}')
            response.raise_for_status()
            r_json = response.json()

            k = r_json.get("exchangeRate")
            for i in k:
                if dict.get('currency') == 'USD':
                        key_buy_exist = 'purchaseRate' in dict
                        key_sale_exist = 'saleRate' in dict
                        if key_buy_exist and key_sale_exist:
                            Rate.objects.create(
                                created=str(d),
                                currency=mch.CURR_USD,
                                buy=dict['purchaseRate'],
                                sale=dict['saleRate'],
                                source=mch.SR_PRIVAT
                            )
                if dict.get('currency') == 'EUR':
                        key_buy_exist = 'purchaseRate' in dict
                        key_sale_exist = 'saleRate' in dict
                        if key_buy_exist and key_sale_exist:
                            Rate.objects.create(
                                created=str(d),
                                currency=mch.CURR_EUR,
                                buy=dict['purchaseRate'],
                                sale=dict['saleRate'],
                                source=mch.SR_PRIVAT
                            )