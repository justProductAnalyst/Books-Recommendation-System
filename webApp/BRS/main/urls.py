from django.urls import path

from . import views
from data.views import api_book_info

urlpatterns = [
    path('', views.index, name='home'),
    path('<int:user_id>', views.index, name='home'),
    path('None', views.login_view, name='home'),
    path('<int:user_id>/history', views.history),
    path('None/history', views.login_view),
    path('about', views.about),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('search/', views.PostIndexView.as_view(), name='post-list'),

    path('book/<str:book_id>', api_book_info, name='post_detail'),
    path('search_books/', views.BlogSearchView.as_view(), name='search_books')
]
