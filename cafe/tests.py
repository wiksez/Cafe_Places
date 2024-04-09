from django.contrib.auth.models import User
from django.http import request
from django.test import TestCase, Client
from django.urls import reverse
import pytest
from cafe.forms import RegistrationForm
from cafe.models import Drinks, Desserts, CoffeeShop, Feedback


# Create your tests here.
def test_index_view():
    client = Client()
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_index_view_for_admin_user():
    user = User.objects.create_user(username='Homer_Simpson')
    user.set_password('password123')
    user.save()
    client = Client()
    url = reverse('home')
    client.login(username='Homer_Simpson', password='password123')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['user_is_admin'] == True


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
def test_drink_list_get(drinks):
    client = Client()
    url = reverse('list_of_drinks')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['drinks'].count() == len(drinks)


def test_add_get_dessert():
    client = Client()
    url = reverse('add_dessert')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_dessert_empty_form_post():
    client = Client()
    url = reverse('add_dessert')
    data = {
        'name': ''
    }
    response = client.post(url, data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_dessert_post():
    client = Client()
    url = reverse('add_dessert')
    data = {
        'name': 'Sernik',
        'description': 'najlepszy w Polsce!!!',
        'composition': 'rodzynki'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('home'))
    assert Desserts.objects.get(name='Sernik', description='najlepszy w Polsce!!!', composition='rodzynki')


@pytest.mark.django_db
def test_dessert_list_get(desserts):
    client = Client()
    url = reverse('list_of_desserts')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['desserts'].count() == len(desserts)


def test_registration_view():
    client = Client()
    url = reverse('registration')
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    assert isinstance(form, RegistrationForm)
    expected_fields = ['username', 'email', 'password1', 'password2']
    for field_name in expected_fields:
        assert field_name in form.fields
