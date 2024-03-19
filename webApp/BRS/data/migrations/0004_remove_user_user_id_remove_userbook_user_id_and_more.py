# Generated by Django 4.2.6 on 2024-03-19 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_alter_user_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='userbook',
            name='user_id',
        ),
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default='', max_length=250, verbose_name='Username'),
        ),
        migrations.AddField(
            model_name='userbook',
            name='username',
            field=models.CharField(default='', max_length=250, verbose_name='Username'),
        ),
    ]
