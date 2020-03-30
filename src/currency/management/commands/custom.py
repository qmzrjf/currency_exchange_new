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
                if i.get('currency') == 'USD':
                    Rate.objects.create(
                        created=str(d),
                        currency=mch.CURR_USD,
                        buy=i['purchaseRate'],
                        sale=i['saleRate'],
                        source=mch.SR_PRIVAT
                    )
                if i.get('currency') == 'EUR':
                    Rate.objects.create(
                        created=str(d),
                        currency=mch.CURR_EUR,
                        buy=i['purchaseRate'],
                        sale=i['saleRate'],
                        source=mch.SR_PRIVAT
                    )
