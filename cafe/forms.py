from django import forms
from cafe.models import Drinks, Desserts
from django.contrib.auth.models import User


class DrinksForm(forms.ModelForm):
    class Meta:
        model = Drinks
        fields = ('name', 'type_is_hot')


class DessertsForm(forms.ModelForm):
    class Meta:
        model = Desserts
        fields = ('name', 'description', 'composition')


class RegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Nazwa użytkownika')
    email = forms.EmailField(label='Adres e-mail')
    password1 = forms.CharField(label='Hasło', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Powtórz hasło', widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
