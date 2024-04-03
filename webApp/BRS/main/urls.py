from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<int:user_id>', views.index, name='home'),
    path('<int:user_id>/history', views.history),
    path('about', views.about),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('search/',  views.PostIndexView.as_view(), name='post-list'),
    path('search/detail/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
    path('search_books/', views.BlogSearchView.as_view(), name='search_books')
]
