from django.urls import reverse
from rest_framework.test import APIClient
import pytest

from account.models import User
from django.core import mail
from account.tasks import send_activation_code_async
from uuid import uuid4

from currency.tasks import _privat, _mono, _alfa, _otp, _pumb, _vkurse


def test_index_page(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_rates_auth(api_client, user):
    url = reverse('api-currency:rates')
    api_client.login(user.email, user.raw_password)
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_rates_not_auth(client):
    url = reverse('api-currency:rates')
    response = client.get(url)
    assert response.status_code == 401
    resp_j = response.json()
    assert len(resp_j) == 1
    assert resp_j['detail'] == 'Authentication credentials were not provided.'


@pytest.mark.django_db
def test_rates(api_client, user):
    url = reverse('api-currency:rates')
    api_client.login(user.email, user.raw_password)
    response = api_client.get(url)
    assert response.status_code == 200

    response_post = api_client.post(url,
                                    data={
                                        "currency": "1",
                                        "buy": "27.80",
                                        "sale": "29.00",
                                        "source": "4"},
                                    format='json', )
    assert response_post.status_code == 201
    assert response_post.json().get("get_currency_display") == "USD"
    assert response_post.json().get("buy") == "27.80"
    assert response_post.json().get("sale") == "29.00"
    assert response_post.json().get("get_source_display") == "OTP"

    url = reverse('api-currency:rate', args=[f'{response_post.json().get("id")}'])
    response_get = api_client.get(url)
    assert response_get.status_code == 200

    response_patch = api_client.patch(url,
                                      data={
                                          "buy": "99.99"},
                                      format='json', )
    assert response_patch.status_code == 200
    assert response_patch.json().get("get_currency_display") == "USD"
    assert response_patch.json().get("buy") == "99.99"
    assert response_patch.json().get("sale") == "29.00"
    assert response_patch.json().get("get_source_display") == "OTP"

    response_put = api_client.put(url,
                                  data={
                                      "currency": "1",
                                      "buy": "27.80",
                                      "sale": "99.00",
                                      "source": "4"},
                                  format='json', )

    assert response_put.status_code == 200
    assert response_put.json().get("get_currency_display") == "USD"
    assert response_put.json().get("buy") == "27.80"
    assert response_put.json().get("sale") == "99.00"
    assert response_put.json().get("get_source_display") == "OTP"

    response_delete = api_client.delete(url)
    assert response_delete.status_code == 204


@pytest.mark.django_db
def test_contacts(api_client, user):
    url = reverse('api-account:contacts')
    api_client.login(user.email, user.raw_password)
    response = api_client.get(url)
    assert response.status_code == 200

    response_post = api_client.post(url,
                                    data={
                                        "email": f'{user.email}',
                                        "subject": "Subject",
                                        "text": "Text"},
                                    format='json', )
    assert response_post.status_code == 201
    assert response_post.json().get("email") == f'{user.email}'
    assert response_post.json().get("subject") == "Subject"
    assert response_post.json().get("text") == "Text"

    url = reverse('api-account:contact', args=[f'{response_post.json().get("id")}'])
    response_get = api_client.get(url)
    assert response_get.status_code == 200

    response_patch = api_client.patch(url,
                                      data={
                                          "text": "Not Text"},
                                      format='json', )
    assert response_patch.status_code == 200
    assert response_patch.json().get("email") == f'{user.email}'
    assert response_patch.json().get("subject") == "Subject"
    assert response_patch.json().get("text") == "Not Text"

    response_put = api_client.put(url,
                                  data={
                                        "email": f'{user.email}',
                                        "subject": "New Subject",
                                        "text": "New Text"},
                                  format='json', )

    assert response_put.status_code == 200
    assert response_put.json().get("email") == f'{user.email}'
    assert response_put.json().get("subject") == "New Subject"
    assert response_put.json().get("text") == "New Text"

    response_delete = api_client.delete(url)
    assert response_delete.status_code == 204


class Response:
    pass


@pytest.mark.django_db
def test_task_privat(mocker):
    def mock():
        response = Response()
        response.json = lambda: [{'ccy': 'USD', 'base_ccy': 'UAH', 'buy': '27.05000', 'sale': '27.50000'},
                                 {'ccy': 'EUR', 'base_ccy': 'UAH', 'buy': '29.25000', 'sale': '29.90000'},
                                 {'ccy': 'RUR', 'base_ccy': 'UAH', 'buy': '0.32000', 'sale': '0.36500'},
                                 {'ccy': 'BTK', 'base_ccy': 'USD', 'buy': '6952.2441', 'sale': '7684.0593'}]

        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()

    _privat()


@pytest.mark.django_db
def test_task_mono(mocker):
    def mock():
        response = Response()
        response.json = lambda: [
            {'currencyCodeA': 840, 'currencyCodeB': 980, 'date': 1586420405, 'rateBuy': 27.2, 'rateSell': 27.4703},
            {'currencyCodeA': 978, 'currencyCodeB': 980, 'date': 1586420405, 'rateBuy': 29.4, 'rateSell': 29.8499},
            {'currencyCodeA': 643, 'currencyCodeB': 980, 'date': 1586380205, 'rateBuy': 0.32, 'rateSell': 0.365},
            {'currencyCodeA': 807, 'currencyCodeB': 980, 'date': 1586428182, 'rateCross': 0.4845}]

        return response

    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = mock()

    _mono()


@pytest.mark.django_db
def test_send_email():
    emails = mail.outbox
    print('EMAILS:', emails)

    send_activation_code_async.delay(1, str(uuid4()))
    emails = mail.outbox
    assert len(emails) == 1

    email = mail.outbox[0]
    assert email.subject == 'Your activation code'

