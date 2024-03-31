from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('add_drink/', views.AddDrinks.as_view(), name="add_drink"),
    path('drinks/', views.DrinksList.as_view(), name="list_of_drinks"),
    path('add_dessert/', views.AddDessert.as_view(), name="add_dessert"),
    path('desserts/', views.DessertsList.as_view(), name="list_of_desserts"),
    path('registration/', views.Registration.as_view(), name="registration"),
    path('cofeeshops/', views.CoffeeShopList.as_view(), name="shops_list"),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout', views.LogoutView.as_view(), name='logout')
]
