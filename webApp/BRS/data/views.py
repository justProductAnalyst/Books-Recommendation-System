from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Book, BookTexts, Reviews
# from BRS.main.models import User
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


def get_book_info_by_book_id(book_id):
    book = Book.objects.filter(book_id=book_id)  # Фильтруем записи по isbn
    serialiser = DataSerializer(book, many=True)  # Используем сериализатор для преобразования данных
    return serialiser.data[0]


def api_book_info(request, book_id):
    book = Book.objects.get(book_id=book_id)
    book_texts = BookTexts.objects.get(book_id=book_id)
    reviews = Reviews.objects.filter(book_id=book_id)

    return render(request, 'main/book_info.html', {'book': book, 'book_texts': book_texts, 'reviews': reviews})


# # @api_view(['GET'])
# def api_book_info(request, book_id):
#     book_data = get_book_info_by_book_id(book_id)
#     return Response(book_data)  # Возвращаем сериализованные данные в ответе на запрос


@api_view(['GET'])
def api_get_recommendations(request, user_id):
    raw = rec_sys.get_recommendations(user_id, n=10)
    print(raw)
    recommendations = [get_book_info_by_book_id(book_id) for book_id in raw]
    return Response(recommendations)  # Возвращаем сериализованные данные в ответе на запрос


@api_view(['GET'])
def api_get_user_history(request, user_id):
    user = get_user_model().objects.get(user_id=user_id)
    username = user.username
    raw = rec_sys.get_user_history(user_id, n=10)
    user_history = [get_book_info_by_book_id(book_id) for book_id in raw]
    response_data = {
        'user_id': user_id,
        'username': username,
        'user_history': user_history
    }
    return JsonResponse(response_data)  # Возвращаем сериализованные данные в ответе на запрос


@api_view(['GET'])
def api_get_popular_books(request):
    raw = rec_sys.get_popular_books(n=10)
    user_history = [get_book_info_by_book_id(book_id) for book_id in raw]
    return Response(user_history)  # Возвращаем сериализованные данные в ответе на запрос
