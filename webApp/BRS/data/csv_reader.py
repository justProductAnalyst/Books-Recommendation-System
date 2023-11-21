import csv
from .models import Book


def import_csv_data(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Пропустить заголовки, если они есть
        for row in reader:
            book = Book(isbn=row[0], title=row[1], image_s=row[5], image_m=row[6], image_l=row[7])
            book.save()
