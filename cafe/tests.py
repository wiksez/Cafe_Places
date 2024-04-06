from django.test import TestCase, Client
from django.urls import reverse
import pytest
from cafe.models import Drinks, Desserts, CoffeeShop, Feedback

# Create your tests here.
def test_index_view():
    client = Client()
    url = reverse('home')
    response = client.get(url)
    assert response.status_code == 200
