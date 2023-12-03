from django.urls import path
from . import views
from django.urls import path
#from .views import import_csv

urlpatterns = [
    path('<int:isbn>', views.data_home, name='data'),
    #path('import-csv/', import_csv, name='import_csv'),
]
