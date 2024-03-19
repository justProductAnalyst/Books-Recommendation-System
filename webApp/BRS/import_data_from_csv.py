import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BRS.settings")
django.setup()

import csv
from data.models import User


with open('data/user_data_orm.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        user = User(
            user_id=row['User-ID'],
            location=row['Location'],
            age=row['Age'],
            password=row['Password']
        )
        user.save()
