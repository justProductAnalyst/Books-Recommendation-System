from django.urls import path
from . import views

urlpatterns = [
    path('<int:isbn>', views.data_home, name='data'),
]
