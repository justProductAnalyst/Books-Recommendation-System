from django.shortcuts import render   #render нужен для вывода html шаблона
from django.http import HttpResponse
# Create your views here.


def index(request, user_id=None):

    # путь прописываем как будто мы в templates
    return render(request, "main/main.html", {'user_id': user_id})

def history(request, user_id=None):
    # путь прописываем как будто мы в templates
    return render(request, "main/user_history.html", {'user_id': user_id})


def about(request):
    return HttpResponse("<h4>About us</h4>")
