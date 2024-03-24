from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('add_drink/', views.AddDrinks.as_view(), name="add_drink"),
    path('drinks/', views.DrinksList.as_view(), name="list_of_drinks")
]
