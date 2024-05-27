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
    book = Book.objects.filter(book_id=book_id).first()  # Получаем первую книгу или None, если книга не найдена
    if book:
        serialiser = DataSerializer(book)  # Используем сериализатор для преобразования данных
        return serialiser.data
    else:
        return {}



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
def api_get_recommendations(request):
    user_id = request.user.user_id
    raw = rec_sys.get_recommendations(user_id, n=10)
    recommendations = [get_book_info_by_book_id(book_id) for book_id in raw]
    return Response(recommendations)  # Возвращаем сериализованные данные в ответе на запрос


@api_view(['GET'])
def api_get_user_history(request):
    user_id = request.user.user_id
    username = request.user.username
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


'''@api_view(['GET'])
def api_search_books(request):
    # Выбираем все книги из базы данных
    books = Book.objects.all()

    # Преобразуем объекты книг в словари
    data = []
    for book in books:
        data.append({
            'book_id': book.book_id,
            'title': book.title,
            'image_s': book.image_s.url if book.image_s else None,
            'image_m': book.image_m.url if book.image_m else None,
            'image_l': book.image_l.url if book.image_l else None,
            'genre': book.genre,
            'author': book.author,
            'year_of_1st_publication': book.year_of_1st_publication
        })

    # Возвращаем JSON ответ
    return JsonResponse({'books': data})
'''

@api_view(['GET'])
def api_search_books(request):
    query = request.GET.get('q', '')
    books = Book.objects.filter(title__icontains=query)[:100]  # Ограничим до 100 книг
    data = [
        {
            'book_id': book.book_id,
            'title': book.title,
            'author': book.author,
        }
        for book in books
    ]
    return JsonResponse(data, safe=False)

