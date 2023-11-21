from django.db import models


# Create your models here.

class User(models.Model):
    sex = models.CharField('Sex', default='kapybara', max_length=250)
    age = models.IntegerField('Age')
    user_id = models.IntegerField('User_id')
    login = models.CharField('login', max_length=250)
    password = models.CharField('password', max_length=250)

    def __str__(self):
        return self.login


class Book(models.Model):
    isbn = models.IntegerField('ISBN')
    title = models.CharField('Title', max_length=100)
    # image_s = models.ImageField('image_s')
    # image_m = models.ImageField('image_m')
    # image_l = models.ImageField('image_l')
    status = models.CharField('Status', max_length=200)
    genre = models.CharField('Genre', max_length=100)

    def __str__(self):
        return self.title
