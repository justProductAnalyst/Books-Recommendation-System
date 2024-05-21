from django.http import HttpResponse
from django.shortcuts import render, redirect  # render нужен для вывода html шаблона
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView

from .forms import CustomUserCreationForm, SearchForm
from django.contrib.auth import authenticate, login, get_user_model
from django.urls import reverse
from django.contrib import messages
from data.models import Book, BookTexts
from .models import User
from .forms import CustomUserCreationForm


# Create your views here.


def index(request, user_id=None):
    # путь прописываем как будто мы в templates
    user = get_user_model()
    if user_id:
        username = user.objects.get(pk=user_id).username
    else:
        username = None
    return render(request, "main/main.html", {'user_id': user_id, 'username': username})


def history(request, user_id=None):
    # путь прописываем как будто мы в templates
    return render(request, "main/user_history.html", {'user_id': user_id})


def about(request):
    return HttpResponse("<h4>About us</h4>")


@csrf_protect
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Не сохраняем пользователя сразу
            user.set_password(form.cleaned_data['password'])  # Хэшируем пароль
            user.save()  # Теперь сохраняем пользователя с хэшированным паролем
            # Дополнительные действия после успешной регистрации
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'main/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page
            user_id = request.user.user_id
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
