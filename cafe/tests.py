from django.contrib.auth.models import User
from django.http import request
from django.test import TestCase, Client
from django.urls import reverse
import pytest
from cafe.forms import RegistrationForm, LoginForm, CommentsForm, DrinksForm, DessertsForm
from cafe.models import Drinks, Desserts, CoffeeShop, Feedback, Favorite


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


@pytest.mark.django_db
def test_add_get_drink():
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    client.login(username='Kot', password='password123')
    url = reverse('add_drink')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_drink_empty_form_post():
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    client.login(username='Kot', password='password123')
    url = reverse('add_drink')
    data = {
        'name': ''
    }
    response = client.post(url, data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_drink_post():
    client = Client()
    Drinks.objects.create(name='Coca-Cola', type_is_hot=False)
    url = reverse('add_drink')
    response = client.post(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('home'))
    assert Drinks.objects.get(name='Coca-Cola', type_is_hot=False)


@pytest.mark.django_db
def test_drink_list_get(drinks):
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    client.login(username='Kot', password='password123')
    url = reverse('list_of_drinks')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['drinks'].count() == len(drinks)


@pytest.mark.django_db
def test_add_get_dessert():
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    client.login(username='Kot', password='password123')
    url = reverse('add_dessert')
    response = client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_dessert_empty_form_post():
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    client.login(username='Kot', password='password123')
    url = reverse('add_dessert')
    data = {
        'name': ''
    }
    response = client.post(url, data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_dessert_post():
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    client.login(username='Kot', password='password123')
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
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    client.login(username='Kot', password='password123')
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


@pytest.mark.django_db
def test_feedback_list(feedbacks):
    client = Client()
    url = reverse('feedbacks')
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    assert isinstance(form, CommentsForm)
    expected_fields = ['comments', 'ranking']
    for field_name in expected_fields:
        assert field_name in form.fields
    assert response.context['comments'].count() == len(feedbacks)


@pytest.mark.django_db
def test_contacts_get(cafe):
    client = Client()
    url = reverse('contacts', kwargs={'id': cafe.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['shop'] == cafe


@pytest.mark.django_db
def test_add_comments_get(cafe):
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    url = reverse('add_feedback', kwargs={'id': cafe.pk})
    client.login(username='Kot', password='password123')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['shop'] == cafe
    form = response.context['form']
    assert isinstance(form, CommentsForm)
    expected_fields = ['comments', 'ranking']
    for field_name in expected_fields:
        assert field_name in form.fields


@pytest.mark.django_db
def test_add_comments_post(cafe):
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    client.login(username='Kot', password='password123')
    url = reverse('add_feedback', kwargs={'id': cafe.pk})
    data = {
        'comments': 'Good.',
        'ranking': '4'
    }
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('home'))


@pytest.mark.django_db
def test_add_comments_post_empty(cafe):
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    client.login(username='Kot', password='password123')
    url = reverse('add_feedback', kwargs={'id': cafe.pk})
    data = {
        'comments': '',
        'ranking': '4'
    }
    response = client.post(url, data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_comments_post_repeat(cafe):
    user = User.objects.create_user(username='Kot')
    Feedback.objects.create(user=user, text='Some comments', coffees=cafe, rating='4')
    user.set_password('password123')
    user.save()
    client = Client()
    client.login(username='Kot', password='password123')
    url = reverse('add_feedback', kwargs={'id': cafe.pk})
    data = {
        'comments': 'Something',
        'ranking': '4'
    }
    response = client.post(url, data)
    assert response.status_code == 200
    assert response.context['message'] == "Już masz opinię o tej kawiarni "


@pytest.mark.django_db
def test_add_cafe_to_favorite(cafe):
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    client.login(username='Kot', password='password123')
    url = reverse('add_favorite_cafe', kwargs={'id': cafe.pk})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('shops_list'))
    favorite_cafe = Favorite.objects.get(user=user)
    assert favorite_cafe.favourite_cafes == cafe


@pytest.mark.django_db
def test_add_drink_to_my_favorite():
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    client.login(username='Kot', password='password123')
    drink = Drinks.objects.create(name="Herbata")
    url = reverse('add_favorite_drink', kwargs={'id': drink.pk})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('my_profile'))
    favorite_drink = Favorite.objects.get(user=user)
    assert favorite_drink.favourite_drinks == drink


@pytest.mark.django_db
def test_add_dessert_to_my_favorite():
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    client.login(username='Kot', password='password123')
    dessert = Desserts.objects.create(name="Sernik")
    url = reverse('add_favorite_dessert', kwargs={'id': dessert.pk})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('my_profile'))
    favorite_dessert = Favorite.objects.get(user=user)
    assert favorite_dessert.favourite_desserts == dessert


@pytest.mark.django_db
def test_my_profile(favorites, user, cafe, feedback):
    client = Client()
    client.login(username='Cukier', password='qwerty1')
    url = reverse('my_profile')
    response = client.get(url)
    assert response.status_code == 200
    assert favorites.favourite_cafes in [item.favourite_cafes for item in response.context['my_cafe']]
    assert favorites.favourite_drinks in [item.favourite_drinks for item in response.context['my_drink']]
    assert favorites.favourite_desserts in [item.favourite_desserts for item in response.context['my_dessert']]
    assert feedback.text in [item.text for item in response.context['my_comments']]


@pytest.mark.django_db
def test_admin_profil():
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    url = reverse('admin_profile')
    response = client.get(url)
    assert response.status_code == 302


@pytest.mark.django_db
def test_update_drink_get(drink):
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    client.login(username='Kot', password='password123')
    url = reverse('update_drink', kwargs={'id': drink.pk})
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    assert isinstance(form, DrinksForm)
    expected_fields = ['name', 'type_is_hot']
    for field_name in expected_fields:
        assert field_name in form.fields


@pytest.mark.django_db
def test_update_drink_post(drink):
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    client.login(username='Kot', password='password123')
    url = reverse('update_drink', kwargs={'id': drink.pk})
    form_data = {
        'name': drink.name,
        'type_is_hot': drink.type_is_hot
    }
    response = client.post(url, form_data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('list_of_drinks'))


@pytest.mark.django_db
def test_update_drink_empty(drink):
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    client.login(username='Kot', password='password123')
    url = reverse('update_drink', kwargs={'id': drink.pk})
    form_data = {
        'name': '',
        'type_is_hot': drink.type_is_hot
    }
    response = client.post(url, form_data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_dessert_get(dessert):
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    client.login(username='Kot', password='password123')
    url = reverse('update_dessert', kwargs={'id': dessert.pk})
    response = client.get(url)
    assert response.status_code == 200
    form = response.context['form']
    assert isinstance(form, DessertsForm)
    expected_fields = ['name', 'description', 'composition']
    for field_name in expected_fields:
        assert field_name in form.fields


@pytest.mark.django_db
def test_update_dessert_post(dessert):
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    client.login(username='Kot', password='password123')
    url = reverse('update_dessert', kwargs={'id': dessert.pk})
    form_data = {
        'name': dessert.name,
        'description': dessert.description,
        'composition': dessert.composition
    }
    response = client.post(url, form_data)
    assert response.status_code == 302
    assert response.url.startswith(reverse('list_of_desserts'))


@pytest.mark.django_db
def test_update_dessert_empty(dessert):
    user = User.objects.create_user(username='Kot')
    user.set_password('password123')
    user.save()
    client = Client()
    client.login(username='Kot', password='password123')
    url = reverse('update_dessert', kwargs={'id': dessert.pk})
    form_data = {
        'name': dessert.name,
        'description': '',
        'composition': dessert.composition
    }
    response = client.post(url, form_data)
    assert response.status_code == 200