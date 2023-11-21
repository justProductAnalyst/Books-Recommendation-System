from django.shortcuts import render   #render нужен для вывода html шаблона
from django.http import HttpResponse
# Create your views here.


def index(request):
    #можем передавать строки, словари, списки
    data = {
        'title': 'main!!',
        'values': [1, 2, 3, 4, 5, 6, 8, 9, 10]
    }
    # путь прописываем как будто мы в templates
    return render(request, "main/main.html", data)


def about(request):
    return HttpResponse("<h4>About us</h4>")
