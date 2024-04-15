# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    # Добавляем related_name для поля groups
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups')

    # Добавляем related_name для поля user_permissions
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions')

    def __str__(self):
        return self.username
