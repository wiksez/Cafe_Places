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
