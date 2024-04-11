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
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('more_details/<int:id>/', views.CoffeShopDetails.as_view(), name='shop_details'),
    path('menu_drinks/<int:id>', views.MenuDrinks.as_view(), name='menu_drinks'),
    path('menu_desserts/<int:id>', views.MenuDesserts.as_view(), name='menu_desserts'),
    path('feedbacks/', views.FeedbacksList.as_view(), name='feedbacks'),
    path('contacts/<int:id>/', views.Contacts.as_view(), name='contacts'),
    path('add_comments/<int:id>/', views.AddComments.as_view(), name='add_feedback'),
    path('add_favorite_cafe/<int:id>/', views.AddCafeToMyFavorite.as_view(), name='add_favorite_cafe'),
    path('my_profile/', views.MyFavoriteCafe.as_view(), name='my_profile'),
    path('admin_profile/', views.AdminSettings.as_view(), name='admin_profile'),
    path('update_drink/<int:id>/', views.UpdateDrinks.as_view(), name='update_drink'),
    path('update_dessert/<int:id>/', views.UpdateDesserts.as_view(), name='update_dessert'),
    path('delete_drink/<int:id>/', views.DeleteDrink.as_view(), name='delete_drink'),
    path('delete_desserts/<int:id>/', views.DeleteDessert.as_view(), name='delete_dessert'),
    path('add_coffeshop/', views.AddCoffeShop.as_view(), name='add_coffeehouse'),
    path('update_cafe/<int:id>/', views.UpdateCoffeShop.as_view(), name='update_cafe'),
    path('delete_cafe/<int:id>/', views.DeleteCafe.as_view(), name='delete_cafe'),
    path('serach/', views.SearchCafe.as_view(), name='search'),
    path('serach_drinks/', views.SearchDrink.as_view(), name='search_drink')
]
