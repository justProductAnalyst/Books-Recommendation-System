# Generated by Django 4.2.6 on 2024-03-19 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.CharField(default='age', max_length=4, verbose_name='Age'),
        ),
    ]
