from rest_framework import serializers
from .models import Book


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('isbn', 'title', 'image_l')
