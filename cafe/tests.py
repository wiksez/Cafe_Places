from django.http import request
from django.test import TestCase, Client
from django.urls import reverse
import pytest

from cafe.forms import DrinksForm
from cafe.models import Drinks, Desserts, CoffeeShop, Feedback

# Create your tests here.
def test_index_view():
    client = Client()
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200


def test_add_get_drink():
    client = Client()
    url = reverse('add_drink')
    response = client.get(url)
    assert response.status_code == 200


def test_add_drink_empty_form_post():
    client = Client()
    url = reverse('add_drink')
    data = {
        'name': ''
    }
    response = client.post(url, data)
    assert response.status_code == 200

@pytest.mark.django_db
def test_add_drink_post():
    client = Client()
    url = reverse('add_drink')
    data = {
        'name': 'Coca-Cola',
        'type_is_hot': False
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('home'))
    assert Drinks.objects.get(name='Coca-Cola', type_is_hot=False)


@pytest.mark.django_db
def test_add_type_get(drinks):
    client = Client()
    url = reverse('list_of_drinks')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['drinks'].count() == len(drinks)
