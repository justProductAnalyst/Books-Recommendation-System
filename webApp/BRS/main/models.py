# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    user_id = models.AutoField(primary_key=True)
    location = models.CharField('Location', max_length=250, default="Vinland", null=True, blank=True)
    age = models.IntegerField('Age', null=True, blank=True)

    def __str__(self):
        return self.username
