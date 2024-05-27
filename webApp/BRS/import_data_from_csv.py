import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BRS.settings")
django.setup()

import csv
from data.models import BookTexts

data = []

with open('data/books_texts_orm.csv', 'r', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        user = BookTexts(
            book_id=row['BookID'],
            description=row['Description'],
            summary=row['Summary'],
        )
        data.append(user)

# Пакетная вставка данных в базу данных
batch_size = 1000
for i in range(0, len(data), batch_size):
    batch = data[i:i+batch_size]
    BookTexts.objects.bulk_create(batch)

