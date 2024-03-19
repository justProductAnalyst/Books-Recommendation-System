from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book
from .serializer import DataSerializer
import sys
import os

# Получаем абсолютный путь к папке 'BRS'
BRS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'BRS'))

# Добавляем путь к папке 'BRS' в sys.path
sys.path.append(BRS_PATH)

# Теперь можно импортировать модуль 'recsys'
from recsys import RecSys

rec_sys = RecSys()


def get_book_info_by_isbn(isbn):
    book = Book.objects.filter(isbn=isbn)  # Фильтруем записи по isbn
    serialiser = DataSerializer(book, many=True)  # Используем сериализатор для преобразования данных
    return serialiser.data[0]


@api_view(['GET'])
def api_book_info(request, isbn):
    book_data = get_book_info_by_isbn(isbn)
    return Response(book_data)  # Возвращаем сериализованные данные в ответе на запрос


@api_view(['GET'])
def api_get_recommendations(request, user_id):
    raw = rec_sys.get_recommendations(user_id, n=10)
    recommendations = [get_book_info_by_isbn(isbn) for isbn in raw]
    return Response(recommendations)  # Возвращаем сериализованные данные в ответе на запрос


@api_view(['GET'])
def api_get_user_history(request, user_id):
    raw = rec_sys.get_user_history(user_id, n=10)
    user_history = [get_book_info_by_isbn(isbn) for isbn in raw]
    return Response(user_history)  # Возвращаем сериализованные данные в ответе на запрос


@api_view(['GET'])
def api_get_popular_books(request):
    raw = rec_sys.get_popular_books(n=10)
    user_history = [get_book_info_by_isbn(isbn) for isbn in raw]
    return Response(user_history)  # Возвращаем сериализованные данные в ответе на запрос
