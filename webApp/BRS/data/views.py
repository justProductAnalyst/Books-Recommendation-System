from django.http import HttpResponse
import csv
from .models import Book
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import render
from rest_framework.response import Response
from .serializer import DataSerializer


@api_view(['GET'])
def data_home(request, isbn):
    book = Book.objects.filter(isbn=isbn)  # Фильтруем записи по isbn
    serializer = DataSerializer(book, many=True)  # Используем сериализатор для преобразования данных
    print(serializer.data)
    return Response(serializer.data)  # Возвращаем сериализованные данные в ответе на запрос


# def import_csv(request):
#     with open('E:/Books-Recommendation-System/webApp/BRS/data/new_merged.csv', encoding="UTF-8") as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             person = Book(
#                 isbn=row['ISBN'],
#                 title=row['Book-Title'],
#                 image_s=row['Image-URL-S'],
#                 image_m=row['Image-URL-M'],
#                 image_l=row['Image-URL-L'],
#                 genre=row['categories'].split("'")[1]
#             )
#             person.save()
#
#     return HttpResponse('CSV imported successfully')

