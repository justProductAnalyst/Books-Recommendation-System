from django import forms
from django.contrib.auth import get_user_model

from .models import User


class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email', 'location', 'age']


class SearchForm(forms.Form):
    query = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Search...'}))

from django import forms

class RatingForm(forms.Form):
    RATING_CHOICES = (
        (1, '1 - awful'),
        (2, '2 - very bad'),
        (3, '3 - bad'),
        (4, '4 - not good'),
        (5, '5 - normal'),
        (6, '6 - not bad'),
        (7, '7 - seven'),
        (8, '8 - good'),
        (9, '9 - very good'),
        (10, '10 - awesome')
    )
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))