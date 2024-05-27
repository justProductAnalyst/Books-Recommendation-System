from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404  # render нужен для вывода html шаблона
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView

from .forms import CustomUserCreationForm, SearchForm, RatingForm, BookSelectionForm
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib import messages
from data.models import Book, BookTexts, UserBook
from .forms import CustomUserCreationForm


# Create your views here.


def index(request, user_id=None):
    # путь прописываем как будто мы в templates
    user_id = request.user.user_id if request.user.is_authenticated else None
    return render(request, "main/main.html", {'user_id': user_id})


def history(request, user_id=None):
    # путь прописываем как будто мы в templates
    user_id = request.user.user_id if request.user.is_authenticated else None
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
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request, user)
            return redirect('choose_books')  # Перенаправляем на страницу выбора книг
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
            # home_url = reverse()
            return redirect('home')
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


def rate_book(request, book_id):
    if not request.user.is_authenticated:
        return redirect('login')
    book = get_object_or_404(Book, book_id=book_id)

    if request.method == 'POST':
        form = RatingForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data['rating']
            user_id = request.user.user_id  # Получаем ID пользователя
            # Сохраняем оценку книги в базе данных
            user_book, created = UserBook.objects.get_or_create(book_id=book_id, user_id=user_id,
                                                                defaults={'rating': rating})
            user_book.rating = rating
            user_book.save()
            # Перенаправляем пользователя на страницу с деталями книги
            return redirect('post_detail', book_id=book.book_id)
    else:
        form = RatingForm()

    return render(request, 'main/rate_book.html', {'book': book, 'form': form})


@login_required
def select_books(request):
    if request.method == 'POST':
        form = BookSelectionForm(request.POST)
        if form.is_valid():
            # Обработка выбранных книг
            # selected_books = form.cleaned_data['books']
            book1_name = form.cleaned_data['book1']
            book2_name = form.cleaned_data['book2']
            book3_name = form.cleaned_data['book3']

            # Выполните поиск книг по введенным названиям
            book1 = Book.objects.filter(book_id=book1_name).first()
            book2 = Book.objects.filter(book_id=book2_name).first()
            book3 = Book.objects.filter(book_id=book3_name).first()
            rating1 = form.cleaned_data['rating1']
            rating2 = form.cleaned_data['rating2']
            rating3 = form.cleaned_data['rating3']
            selected_books = [book1, book2, book3]
            user_id = request.user.user_id
            UserBook.objects.create(book_id=book1.book_id, user_id=user_id, rating=float(rating1))
            UserBook.objects.create(book_id=book2.book_id, user_id=user_id, rating=float(rating2))
            UserBook.objects.create(book_id=book3.book_id, user_id=user_id, rating=float(rating3))
            return redirect('home')
    else:
        form = BookSelectionForm()
    return render(request, 'main/select_books.html', {'form': form})
