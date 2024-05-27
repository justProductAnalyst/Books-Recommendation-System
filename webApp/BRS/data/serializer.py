from rest_framework import serializers

from .models import Book


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('book_id', 'title', 'image_l')
