from . import views
from django.urls import path
#from .views import import_csv

urlpatterns = [
    path('book/<int:isbn>', views.api_book_info, name='data'),
    path('recommendations/<int:user_id>', views.api_get_recommendations, name='data'),
    #path('import-csv/', import_csv, name='import_csv'),
]
