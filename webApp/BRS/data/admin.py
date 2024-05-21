from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import  Book, BookTexts, UserBook, Reviews

# Register your models here.

admin.site.register(Book)
admin.site.register(BookTexts)
admin.site.register(UserBook)
admin.site.register(Reviews)
