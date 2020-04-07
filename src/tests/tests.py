from django.urls import reverse
from rest_framework.test import APIClient
import pytest


def test_sanity():
    assert 200 == 200


def test_index_page(client):
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_get_rates(client):
    url = reverse('api-currency:rates')
    response = client.get(url)
    # resp_j = response.json()
    assert response.status_code == 401
    # assert len(resp_j) == 1

@pytest.mark.django_db
def test_rates_auth(api_client, user):

    url = reverse('api-currency:rates')
    api_client.login(user.email, user.raw_password)
    response = api_client.get(url)
    assert response.status_code == 200


# @pytest.mark.django_db
# def test_get_rates(api_client):
#
#     url = reverse('api-currency:rates')