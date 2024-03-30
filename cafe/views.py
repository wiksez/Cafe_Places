from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View

from cafe.forms import DrinksForm, DessertsForm, RegistrationForm
from cafe.models import Drinks, Desserts, CoffeeShop

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


class Registration(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            pass1 = form.cleaned_data.get('password1')
            pass2 = form.cleaned_data.get('password2')
            if pass1 is not None and pass1 == pass2:
                user.set_password(pass1)
                user.save()
                return redirect('home')
        return render(request, 'registration.html', {'form': form})


class CoffeeShopList(View):
    def get(self, request):
        cofeshops = CoffeeShop.objects.all()
        return render(request, 'coffeeshops.html', {'shops': cofeshops})

