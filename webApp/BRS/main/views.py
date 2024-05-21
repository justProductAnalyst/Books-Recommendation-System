from django.http import HttpResponse
from django.shortcuts import render, redirect  # render нужен для вывода html шаблона
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView

from .forms import RegistrationForm, SearchForm
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib import messages
from data.models import Book, BookTexts
from django.contrib.auth.models import User


# Create your views here.


def index(request, user_id=None):
    # путь прописываем как будто мы в templates
    return render(request, "main/main.html", {'user_id': user_id})


def history(request, user_id=None):
    # путь прописываем как будто мы в templates
    return render(request, "main/user_history.html", {'user_id': user_id})


def about(request):
    return HttpResponse("<h4>About us</h4>")


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            email = form.cleaned_data.get('email')
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)  # Хэширование пароля
            user.save()
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


class BlogSearchView(ListView):
    model = Book
    template_name = 'main/search.html'
    context_object_name = 'books'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return Book.objects.filter(title__icontains=query).order_by('-title')


class PostIndexView(ListView):
    model = Book
    template_name = 'main/search.html'
    queryset = Book.objects.filter(title__icontains="the+martian").order_by('-title')
    context_object_name = 'books'


class PostDetailView(DetailView):
    model = BookTexts
    context_object_name = 'book'
    template_name = 'main/search_results.html'
