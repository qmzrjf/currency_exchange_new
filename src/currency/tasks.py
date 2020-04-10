from decimal import Decimal

import requests
from celery import shared_task
from bs4 import BeautifulSoup

from currency.models import Rate
from currency import model_choices as mch


from currency_exchange.settings import BASE_DIR

def _append_db(rate_kwargs, currency, code, sourse_string, sorse_bank):
    new_rate = Rate(**rate_kwargs)
    last_rate = Rate.objects.filter(currency=currency, source=sorse_bank).last()

    print(f'{sourse_string} {code} cheked.')
    if last_rate is None or (new_rate.buy != last_rate.buy or new_rate.sale != last_rate.sale):
        new_rate.save()
        print(f'{sourse_string} {code} update!')
    else:
        print(f'{sourse_string} {code} no changes.')


@shared_task()
def _privat():
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)
    r_json = response.json()

    for rate in r_json:
        if rate['ccy'] in {'USD', 'EUR'}:
            currency = {
                'USD': mch.CURR_USD,
                'EUR': mch.CURR_EUR,
            }[rate['ccy']]
            code = mch.CURRENCY_CHOICES_DICT[currency]
            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(rate['buy']),
                'sale': Decimal(rate['sale']),
                'source': mch.SR_PRIVAT,
            }
            _append_db(rate_kwargs, currency, code, 'Privat', mch.SR_PRIVAT)


@shared_task()
def _mono():
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)
    r_json = response.json()
    for rate in r_json:
        if rate['currencyCodeA'] in {840, 978} and rate['currencyCodeB'] == 980:
            mono_code = {
                840: mch.CURR_USD,
                978: mch.CURR_EUR,
            }

            currency = mono_code[rate['currencyCodeA']]
            code = mch.CURRENCY_CHOICES_DICT[currency]

            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(str(round(rate['rateBuy'], 2))),
                'sale': Decimal(str(round(rate['rateSell'], 2))),
                'source': mch.SR_MONO,
            }
            _append_db(rate_kwargs, currency, code, 'Mono', mch.SR_MONO)


@shared_task()
def _vkurse():
    url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(url)
    r_json = response.json()
    for i in r_json:
        if i in {'Dollar', 'Euro'}:
            k = r_json.get(i)
            vkurse_code = {
                'Dollar': mch.CURR_USD,
                'Euro': mch.CURR_EUR,
            }
            cur_buy = k.get('buy')
            cur_sell = k.get('sale')

            cur_buy = ''.join(x for x in cur_buy if x.isdigit() or x == '.')
            cur_sell = ''.join(x for x in cur_sell if x.isdigit() or x == '.')

            currency = vkurse_code[i]
            code = mch.CURRENCY_CHOICES_DICT[currency]
            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(cur_buy),
                'sale': Decimal(cur_sell),
                'source': mch.SR_VKUR,
            }
            _append_db(rate_kwargs, currency, code, 'Vkurse', mch.SR_VKUR)


@shared_task()
def _otp():
    url = 'https://www.otpbank.com.ua/'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    p = soup.find_all('option')
    cur_list = ['USD', 'EUR']
    from pdb import set_trace
    set_trace()
    for th in p:
        q = th.attrs
        # from pdb import set_trace
        # set_trace()
        cur = q.get('value')
        if cur in cur_list:
            vkurse_code = {
                'USD': mch.CURR_USD,
                'EUR': mch.CURR_EUR,
            }

            currency = vkurse_code[cur]
            code = mch.CURRENCY_CHOICES_DICT[currency]
            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(str(round(float(q['buy']), 2))),
                'sale': Decimal(str(round(float(q['sale']), 2))),
                'source': mch.SR_OTP,
            }
            cur_list.remove(cur)
            _append_db(rate_kwargs, currency, code, 'OTP', mch.SR_OTP)


@shared_task()
def _pumb():

    url = 'https://www.pumb.ua/'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    p = soup.find_all('table')
    q = enumerate(p[0].get_text().split())
    list_1, list_2 = [], []

    for i in q:
        if 2 <= i[0] <= 4:
            list_1.append(i[1])
        elif 5 <= i[0] <= 7:
            list_2.append(i[1])
    list_all = [list_1, list_2]
    list_dict = []
    for x in list_all:
        dict_x = {'value': x[0], 'buy': x[1], 'sale': x[2]}
        list_dict.append(dict_x)

    cur_list = {'USD', 'EUR'}
    for th in list_dict:
        cur = th.get('value')
        if cur in cur_list:
            vkurse_code = {
                'USD': mch.CURR_USD,
                'EUR': mch.CURR_EUR,
            }
            # from pdb import set_trace
            # set_trace()
            currency = vkurse_code[cur]
            code = mch.CURRENCY_CHOICES_DICT[currency]
            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(th.get('buy')),
                'sale': Decimal(th.get('sale')),
                'source': mch.SR_PUMB,
            }
            _append_db(rate_kwargs, currency, code, 'PUMB', mch.SR_PUMB)


@shared_task()
def _alfa():
    url = 'https://alfabank.ua/currency-exchange'
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')
    p = soup.find_all('span', class_='rate-number')
    dict_usd = {'value': 'USD'}
    dict_eur = {'value': 'EUR'}
    for th in p:
        q = th.attrs
        if q['data-currency'] == 'USD_BUY':
            dict_usd['buy'] = float(th.get_text())
        elif q['data-currency'] == 'USD_SALE':
            dict_usd['sale'] = float(th.get_text())
        elif q['data-currency'] == 'EUR_BUY':
            dict_eur['buy'] = float(th.get_text())
        elif q['data-currency'] == 'EUR_SALE':
            dict_eur['sale'] = float(th.get_text())

    list_dict = [dict_usd, dict_eur]
    cur_list = ['USD', 'EUR']
    for th in list_dict:
        cur = th.get('value')
        if cur in cur_list:
            vkurse_code = {
                'USD': mch.CURR_USD,
                'EUR': mch.CURR_EUR,
            }

            currency = vkurse_code[cur]
            code = mch.CURRENCY_CHOICES_DICT[currency]
            rate_kwargs = {
                'currency': currency,
                'buy': Decimal(str(round(th['buy'], 2))),
                'sale': Decimal(str(round(th['sale'], 2))),
                'source': mch.SR_ALFA,
            }
            _append_db(rate_kwargs, currency, code, 'Alfa', mch.SR_ALFA)


@shared_task()
def parse_rates():
    # _privat.delay()
    # _mono.delay()
    # _vkurse.delay()
    # _otp.delay()
    # _pumb.delay()
    # _alfa.delay()
    _privat()
    _mono()
    _vkurse()
    _otp()
    _pumb()
    _alfa()
