from django.contrib import admin

from .models import User, Book, BookTexts, UserBook, Reviews

# Register your models here.
admin.site.register(User)
admin.site.register(Book)
admin.site.register(BookTexts)
admin.site.register(UserBook)
admin.site.register(Reviews)
