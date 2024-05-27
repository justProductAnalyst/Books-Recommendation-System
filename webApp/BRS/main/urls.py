from django.urls import path

from . import views
from data.views import api_book_info
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name='home'),
    path('history', views.history, name='history'),
    path('about', views.about),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('search/', views.PostIndexView.as_view(), name='post-list'),
    path('book/<str:book_id>', api_book_info, name='post_detail'),
    path('search_books/', views.BlogSearchView.as_view(), name='search_books'),
    path('book/<str:book_id>/rate/', views.rate_book, name='rate_book'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('select_books/', views.select_books, name='choose_books'),
]
