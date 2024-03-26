from django.http import HttpResponse
from django.shortcuts import render, redirect  # render нужен для вывода html шаблона
from .forms import RegistrationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib import messages

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


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page
            user_id = request.user.id
            home_url = reverse('home', args=[user_id])
            return redirect(home_url)
        else:
            # Return an error message
            messages.error(request, 'Неверные учетные данные. Пожалуйста, попробуйте еще раз.')
    return render(request, 'main/login.html')
