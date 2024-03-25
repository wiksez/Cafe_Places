from django import forms
from cafe.models import Drinks, Desserts


class DrinksForm(forms.ModelForm):
    class Meta:
        model = Drinks
        fields = ('name', 'type_is_hot')


class DessertsForm(forms.ModelForm):
    class Meta:
        model = Desserts
        fields = ('name', 'description', 'composition')
