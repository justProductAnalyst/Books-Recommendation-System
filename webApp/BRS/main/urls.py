from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('<int:user_id>', views.index, name='home'),
    path('<int:user_id>/history', views.history),
    path('about', views.about),
    path('register/', views.register, name='register'),
]
