from django import forms
from cafe.models import Drinks


class DrinksForm(forms.ModelForm):
    class Meta:
        model = Drinks
        fields = ('name', 'type_is_hot')
