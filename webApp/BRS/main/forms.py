from django import forms
from django.contrib.auth import get_user_model

from data.models import Book
from data.views import api_get_popular_books

class CustomUserCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'email', 'location', 'age']


class SearchForm(forms.Form):
    query = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Search...'}))


class RatingForm(forms.Form):
    RATING_CHOICES = (
        (1, '1 - awful'),
        (2, '2 - very bad'),
        (3, '3 - bad'),
        (4, '4 - not good'),
        (5, '5 - normal'),
        (6, '6 - not bad'),
        (7, '7 - nice'),
        (8, '8 - good'),
        (9, '9 - very good'),
        (10, '10 - awesome')
    )
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))


class BookSelectionForm(forms.Form):
    book1 = forms.CharField(label='Книга 1', max_length=100, required=True)
    book2 = forms.CharField(label='Книга 2', max_length=100, required=True)
    book3 = forms.CharField(label='Книга 3', max_length=100, required=True)
    RATING_CHOICES = (
        (1, '1 - awful'),
        (2, '2 - very bad'),
        (3, '3 - bad'),
        (4, '4 - not good'),
        (5, '5 - normal'),
        (6, '6 - not bad'),
        (7, '7 - nice'),
        (8, '8 - good'),
        (9, '9 - very good'),
        (10, '10 - awesome')
    )
    rating1 = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    rating2 = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    rating3 = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))