from django.contrib.auth.models import User
from django.http import request
from django.test import TestCase, Client
from django.urls import reverse
import pytest
from cafe.forms import RegistrationForm, LoginForm, CommentsForm
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


@pytest.mark.django_db
def test_registration_post():
    client = Client()
    url = reverse('registration')
    data = {
        'username': 'Nick',
        'email': 'nick@mail.com',
        'password1': 'qwerty123',
        'password2': 'qwerty123'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('home'))
    assert User.objects.count() == 1
    assert User.objects.filter(username='Nick', email='nick@mail.com').exists()


@pytest.mark.django_db
def test_registration_post_wrong_password():
    client = Client()
    url = reverse('registration')
    data = {
        'username': 'Nick',
        'email': 'nick@mail.com',
        'password1': 'qwerty123',
        'password2': '321'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_registration_post_empty():
    client = Client()
    url = reverse('registration')
    data = {
        'username': '',
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert User.objects.count() == 0


@pytest.mark.django_db
def test_coffeehouses_list_get(coffeehouses):
    client = Client()
    url = reverse('shops_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['shops'].count() == len(coffeehouses)


@pytest.mark.django_db
def test_coffeehouses_list_for_admin():
    user = User.objects.create_user(username='Homer_Simpson')
    user.set_password('password123')
    user.save()
    client = Client()
    url = reverse('shops_list')
    client.login(username='Homer_Simpson', password='password123')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['user_is_admin'] == True


def test_login_get():
    client = Client()
    url = reverse('login')
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    assert isinstance(form, LoginForm)
    expected_fields = ['username', 'password']
    for field_name in expected_fields:
        assert field_name in form.fields


@pytest.mark.django_db
def test_login_post(user):
    client = Client()
    redirect_url = reverse('login')
    data = {
        'username': 'Cukier',
        'password': 'qwerty1'
    }
    response = client.post(redirect_url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('home'))


@pytest.mark.django_db
def test_login_post_wrong(user):
    client = Client()
    redirect_url = reverse('login')
    data = {
        'username': 'Cukier',
        'password': '123'
    }
    response = client.post(redirect_url, data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_logout(user):
    client = Client()
    url = reverse('logout')
    client.login(username='Cukier', password='qwerty1')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('home'))


@pytest.mark.django_db
def test_menu_drinks(drinks):
    client = Client()
    cafe = CoffeeShop.objects.create(name="Some_cafe", description="abc", adres="Legnicka", phone_number="123456789",
                                     district="Fabryczna", start_of_work="09:00", end_of_work="18:00")
    cafe.drinks.add(*drinks)
    url = reverse('menu_drinks', kwargs={'id': cafe.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['shop'] == cafe
    assert response.context['drinks'].count() == len(drinks)


@pytest.mark.django_db
def test_menu_desserts(desserts):
    client = Client()
    cafe = CoffeeShop.objects.create(name="Some_cafe", description="abc", adres="Legnicka", phone_number="123456789",
                                     district="Fabryczna", start_of_work="09:00", end_of_work="18:00")
    cafe.desserts.add(*desserts)
    url = reverse('menu_desserts', kwargs={'id': cafe.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['shop'] == cafe
    assert response.context['desserts'].count() == len(desserts)


@pytest.mark.django_db
def test_cafe_details(drinks, desserts, cafe, feedback):
    client = Client()
    cafe = cafe
    cafe.desserts.add(*desserts)
    cafe.drinks.add(*drinks)
    comment = feedback
    url = reverse('shop_details', kwargs={'id': cafe.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['shop'] == cafe
    assert response.context['desserts'].count() == len(desserts)
    assert response.context['drinks'].count() == len(drinks)
    assert comment.text in [item.text for item in response.context['comments']]