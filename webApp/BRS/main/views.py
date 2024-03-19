from django.http import HttpResponse
from django.shortcuts import render, redirect  # render нужен для вывода html шаблона
from .forms import RegistrationForm


# Create your views here.


def index(request, user_id=None):
    # путь прописываем как будто мы в templates
    return render(request, "main/main.html", {'user_id': user_id})


def history(request, user_id=None):
    # путь прописываем как будто мы в templates
    return render(request, "main/user_history.html", {'user_id': user_id})


def about(request):
    return HttpResponse("<h4>About us</h4>")


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Перенаправление на главную страницу после успешной регистрации
    else:
        form = RegistrationForm()

    return render(request, 'main/register.html', {'form': form})
