from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth import authenticate, login, logout

from cafe.forms import DrinksForm, DessertsForm, RegistrationForm, LoginForm, CommentsForm, CoffeShopForm, SearchCoffeeForm
from cafe.models import Drinks, Desserts, CoffeeShop, Feedback, Favorite
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

# Create your views here.
"""
A. użytkownik nie zarejestrowany. Ma dostęp do następnych widoków:
        1. Lista kawiarni
        2. poszukiwanie drinka
        3. Lista drinków oraz deserów w kawiarni
        4. Czytanie opinii od innych użytkowników
        5. Sortowanie kawiarni według dzielnicy
B. użytkownik zarejestrowany. Ma dodatkowo dostęp do następnych widoków:
        1. Napisanie opinii do kawiarni
        2. Wystawienie oceny
        3. Może mieć własną listę ulubionych kawiarni, drinka oraz desera
        4. Lista z własnymi komentarzami na swoim profilu
C. 1 administrator może:
        1. Dodawać kawiarni, drinki, desery
        2. Zmieniać jakąkolwiek informacje w kawiarniach, meni
        3. Usuwać kawiarni, drinki oraz desery z listy
"""


def index(request):
    if request.user.username == 'Homer_Simpson':
        return render(request, 'main.html', {'user_is_admin': True})
    else:
        return render(request, 'main.html', {'user_is_admin': False})


class AddDrinks(LoginRequiredMixin, View):

    def get(self, request):
        form = DrinksForm()
        return render(request, 'add_drink.html', {'form': form})

    def post(self, request):
        form = DrinksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'add_drink.html', {'form': form})


class DrinksList(LoginRequiredMixin, View):
    def get(self, request):
        drinks = Drinks.objects.all()
        return render(request, 'drinks_list.html', {'drinks': drinks})


class AddDessert(LoginRequiredMixin, View):
    def get(self, request):
        form = DessertsForm()
        return render(request, 'add_dessert.html', {'form': form})

    def post(self, request):
        form = DessertsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, 'add_dessert.html', {'form': form})


class DessertsList(LoginRequiredMixin, View):
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
        if request.user.username == 'Homer_Simpson':
            return render(request, 'coffeeshops.html', {'shops': cofeshops, 'user_is_admin': True})
        else:
            return render(request, 'coffeeshops.html', {'shops': cofeshops, 'user_is_admin': False})


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        redirect_url = request.GET.get('next', reverse('home'))
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(redirect_url)
        return render(request, 'registration.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')


class MenuDrinks(View):
    def get(self, request, id):
        shop = CoffeeShop.objects.get(pk=id)
        drinks = shop.drinks.all()
        return render(request, 'menu_drinks.html', {'shop': shop, 'drinks': drinks})


class MenuDesserts(View):
    def get(self, request, id):
        shop = CoffeeShop.objects.get(pk=id)
        desserts = shop.desserts.all()
        return render(request, 'menu_desserts.html', {'shop': shop, 'desserts': desserts})


class CoffeShopDetails(View):
    def get(self, request, id):
        shop = CoffeeShop.objects.get(pk=id)
        drinks = shop.drinks.all()
        desserts = shop.desserts.all()
        comments = Feedback.objects.filter(coffees=shop)
        form = CommentsForm()
        return render(request, 'coffe_shop_details.html',
                      {'shop': shop, 'drinks': drinks, 'desserts': desserts, 'comments': comments, 'form': form})


class FeedbacksList(View):
    def get(self, request):
        form = CommentsForm()
        comments = Feedback.objects.all()
        return render(request, 'feedbacks.html', {'comments': comments, 'form': form})


class Contacts(View):
    def get(self, request, id):
        shop = CoffeeShop.objects.get(pk=id)
        return render(request, 'contacts.html', {'shop': shop})


class AddComments(LoginRequiredMixin, View):
    def get(self, request, id):
        shop = CoffeeShop.objects.get(pk=id)
        form = CommentsForm()
        return render(request, 'add_comment.html', {'shop': shop, 'form': form})

    def post(self, request, id):
        form = CommentsForm(request.POST)
        shop = CoffeeShop.objects.get(pk=id)
        sum_of_grades = 0
        try:
            if form.is_valid():
                comment = form.cleaned_data['comments']
                rating = form.cleaned_data['ranking']
                new_feedback = Feedback.objects.create(user=request.user, text=comment, coffees=shop, rating=rating)
                new_feedback.save()
                grades = Feedback.objects.filter(coffees=shop).values_list('rating', flat=True)
                for grade in grades:
                    sum_of_grades += int(grade)
                shop.ranking = sum_of_grades / len(grades)
                shop.save()
                return redirect('home')
        except IntegrityError:
            message = "Już masz opinię o tej kawiarni "
            return render(request, 'add_comment.html', {'message': message, 'shop': shop, 'form': form})
        return render(request, 'add_comment.html', {'shop': shop, 'form': form})


class AddCafeToMyFavorite(LoginRequiredMixin, View):
    def get(self, request, id):
        cafe = CoffeeShop.objects.get(pk=id)
        user = request.user
        my_cafe, created = Favorite.objects.get_or_create(user=user)
        if created:
            my_cafe.favourite_cafes = cafe
            my_cafe.save()
        else:
            my_cafe.favourite_cafes = cafe
            my_cafe.save()
        return redirect('shops_list')


class AddDrinkToMyFavorite(LoginRequiredMixin, View):
    def get(self, request, id):
        drink = Drinks.objects.get(pk=id)
        user = request.user
        my_drink, created = Favorite.objects.get_or_create(user=user)
        if created:
            my_drink.favourite_drinks = drink
            my_drink.save()
        else:
            my_drink.favourite_drinks = drink
            my_drink.save()
        return redirect('my_profile')


class AddDessertToMyFavorite(LoginRequiredMixin, View):
    def get(self, request, id):
        dessert = Desserts.objects.get(pk=id)
        user = request.user
        my_dessert, created = Favorite.objects.get_or_create(user=user)
        if created:
            my_dessert.favourite_desserts = dessert
            my_dessert.save()
        else:
            my_dessert.favourite_desserts = dessert
            my_dessert.save()
        return redirect('my_profile')


class MyProfile(LoginRequiredMixin, View):
    def get(self, request):
        cafe = Favorite.objects.filter(user=request.user)
        drink = Favorite.objects.filter(user=request.user)
        dessert = Favorite.objects.filter(user=request.user)
        comments = Feedback.objects.filter(user=request.user)
        return render(request, 'my_profile.html', {'my_cafe': cafe, 'my_drink': drink, 'my_dessert': dessert, 'my_comments': comments})


class AdminSettings(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin_profile.html')


class UpdateDrinks(LoginRequiredMixin, View):
    def get(self, request, id):
        drink = Drinks.objects.get(pk=id)
        form = DrinksForm(instance=drink)
        return render(request, 'update_drink.html', {'form': form})

    def post(self, request, id):
        drink = Drinks.objects.get(pk=id)
        form = DrinksForm(request.POST, instance=drink)
        if form.is_valid():
            form.save()
            return redirect('list_of_drinks')
        return render(request, 'update_drink.html', {'form': form})


class UpdateDesserts(LoginRequiredMixin, View):
    def get(self, request, id):
        dessert = Desserts.objects.get(pk=id)
        form = DessertsForm(instance=dessert)
        return render(request, 'update_dessert.html', {'form': form})

    def post(self, request, id):
        dessert = Desserts.objects.get(pk=id)
        form = DessertsForm(request.POST, instance=dessert)
        if form.is_valid():
            form.save()
            return redirect('list_of_desserts')
        return render(request, 'update_dessert.html', {'form': form})


class DeleteDrink(LoginRequiredMixin, View):
    def get(self, request, id):
        drink = Drinks.objects.get(pk=id)
        drink.delete()
        return redirect('list_of_drinks')


class DeleteDessert(LoginRequiredMixin, View):
    def get(self, request, id):
        dessert = Desserts.objects.get(pk=id)
        dessert.delete()
        return redirect('list_of_desserts')


class AddCoffeShop(LoginRequiredMixin, View):
    def get(self, request):
        form = CoffeShopForm()
        return render(request, 'add_coffeshop.html', {'form': form})

    def post(self, request):
        form = CoffeShopForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shops_list')
        return render(request, 'add_coffeshop.html', {'form': form})


class UpdateCoffeShop(LoginRequiredMixin, View):
    def get(self, request, id):
        cafe = CoffeeShop.objects.get(pk=id)
        form = CoffeShopForm(instance=cafe)
        return render(request, 'update_cafe.html', {'form': form})

    def post(self, request, id):
        cafe = CoffeeShop.objects.get(pk=id)
        form = CoffeShopForm(request.POST, instance=cafe)
        if form.is_valid():
            form.save()
            return redirect('shops_list')
        return render(request, 'update_cafe.html', {'form': form})


class DeleteCafe(LoginRequiredMixin, View):
    def get(self, request, id):
        cafe = CoffeeShop.objects.get(pk=id)
        cafe.delete()
        return redirect('shops_list')


class SearchCafe(View):
    def get(self, request):
        return render(request, 'search.html')

    def post(self, request):
        cafe = CoffeeShop.objects.all()
        selected_districts = []
        if 'stare_miasto' in request.POST:
            selected_districts.append('Stare Miasto')
        if 'srodmiescie' in request.POST:
            selected_districts.append('Śródmieście')
        if 'krzyki' in request.POST:
            selected_districts.append('Krzyki')
        if 'fabryczna' in request.POST:
            selected_districts.append('Fabryczna')
        if 'psie_pole' in request.POST:
            selected_districts.append('Psie Pole')
        if len(selected_districts) == 0:
            cafes = CoffeeShop.objects.all()
        else:
            cafes = CoffeeShop.objects.filter(district__in=selected_districts)
        return render(request, 'search.html', {'cafes': cafes})


class SearchDrink(View):
    def get(self, request):
        form = SearchCoffeeForm()
        return render(request, 'search_drink.html', {'form': form})

    def post(self, request):
        cafe = CoffeeShop.objects.all()
        form = SearchCoffeeForm(request.POST)
        if form.is_valid():
            drink = form.cleaned_data.get('drink')
            cafe_with_drink = cafe.filter(drinks__name=drink)
            if cafe_with_drink.exists():
                return render(request, 'search_drink.html', {'form': form, 'cafes': cafe_with_drink})
            else:
                message = f"Nie ma na naszej stronie kawiarni z napojem '{drink}'."
                return render(request, 'search_drink.html', {'form': form, 'message': message})