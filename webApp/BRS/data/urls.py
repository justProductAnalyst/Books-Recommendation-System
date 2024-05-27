from django.urls import path

from . import views

urlpatterns = [
    path('book/<str:book_id>', views.api_book_info, name='data'),
    path('recommendations/', views.api_get_recommendations, name='data'),
    path('recommendations/<int:user_id>', views.api_get_recommendations, name='data'),
    path('history/', views.api_get_user_history, name='data'),
    path('popular/', views.api_get_popular_books, name='data'),
    path('search/', views.api_search_books, name='data')
    #path('import-csv/', import_csv, name='import_csv'),
]
