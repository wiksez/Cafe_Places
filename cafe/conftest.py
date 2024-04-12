import pytest
from django.contrib.auth.models import User

from cafe.models import Drinks, Desserts, CoffeeShop, Feedback


@pytest.fixture
def drinks():
    drinks = []
    for x in range(5):
        drinks.append(Drinks.objects.create(name=x))
    return drinks


@pytest.fixture
def desserts():
    dessert = []
    for x in range(5):
        dessert.append(Desserts.objects.create(name=x))
    return dessert


@pytest.fixture()
def coffeehouses():
    cafe = []
    for x in range(5):
        cafe.append(CoffeeShop.objects.create(
            name='name',
            description="abc",
            adres="Legnicka",
            phone_number="123456789",
            district="Fabryczna",
            start_of_work="09:00",
            end_of_work="18:00"
        ))
    return cafe


@pytest.fixture
def user():
    user = User.objects.create(username='Cukier')
    user.set_password('qwerty1')
    user.save()
    return user


@pytest.fixture
def cafe():
    cafe = CoffeeShop.objects.create(
            name='name',
            description="abc",
            adres="Legnicka",
            phone_number="123456789",
            district="Fabryczna",
            start_of_work="09:00",
            end_of_work="18:00"
        )
    return cafe


@pytest.fixture
def feedback(user, cafe):
    feedback = Feedback.objects.create(user=user, text="good", coffees=cafe, rating=4)
    return feedback
