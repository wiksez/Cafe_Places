import pytest
from django.contrib.auth.models import User

from cafe.models import Drinks, Desserts, CoffeeShop, Feedback, Favorite


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


@pytest.fixture
def feedbacks(cafe):
    comments = []
    for x in range(5):
        user = User.objects.create(username=x)
        user.set_password(f'qwerty{x}')
        user.save()
        comments.append(Feedback.objects.create(user=user, text=x, coffees=cafe, rating=x))
    return comments


@pytest.fixture
def favorites(user, cafe):
    drink = Drinks.objects.create(name="Cola")
    dessert = Desserts.objects.create(name="sernik")
    my_favorite = Favorite.objects.create(user=user, favourite_cafes=cafe, favourite_desserts=dessert, favourite_drinks=drink)
    return my_favorite


@pytest.fixture
def drink():
    drink = Drinks.objects.create(name="Cola")
    return drink


@pytest.fixture
def dessert():
    drink = Desserts.objects.create(name="Sernik", description='pyszny', composition='cream')
    return drink