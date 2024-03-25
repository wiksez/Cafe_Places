from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from cafe.forms import DrinksForm, DessertsForm
from cafe.models import Drinks, Desserts

# Create your views here.
"""
A. użytkownik nie zarejestrowany. Ma dostęp do następnych widoków:
        1. Lista kawiarni
        2. poszukiwanie kawiarni, drinka lub desera
        3. Lista drinków oraz deserów w kawiarni
        4. Czytanie opinii od innych użytkowników
        5. Sortowanie kawiarni według rankinga, dzielnicy
B. użytkownik zarejestrowany. Ma dodatkowo dostęp do następnych widoków:
        1. Napisanie opinii do kawiarni
        2. Wystawienie oceny
        3. Może mieć własną liste ulubionych kawiarni, drinków oraz deserów
        4. Naprawienia lub usunięcia komentaża oraz oceny
C. 2-3 administratora mogą:
        1. Dodawać kawiarni, drinki, dessery
        2. Zmienać jakąkolwiek informacje w kawiarniach, meni
        3. Usuwać kawiarni, drinki oraz dessery z listy, usuwać użytkownika, ich oceny i opinii
"""


def index(request):
    return render(request, 'main.html')


class AddDrinks(View):

    def get(self, request):
        form = DrinksForm()
        return render(request, 'add_drink.html', {'form': form})

    def post(self, request):
        form = DrinksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')


class DrinksList(View):
    def get(self, request):
        drinks = Drinks.objects.all()
        return render(request, 'drinks_list.html', {'drinks': drinks})


class AddDessert(View):
    def get(self, request):
        form = DessertsForm()
        return render(request, 'add_dessert.html', {'form': form})

    def post(self, request):
        form = DessertsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')


class DessertsList(View):
    def get(self, request):
        desserts = Desserts.objects.all()
        return render(request, 'desserts_list.html', {'desserts': desserts})

