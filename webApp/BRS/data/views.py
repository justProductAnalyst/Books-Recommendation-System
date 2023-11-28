from django.http import HttpResponse
import csv
from .models import Book


def data_home(request, isbn):
    return HttpResponse(f"<h4>Some info about book {isbn}</h4>")


def import_csv(request):
    with open('E:/Books-Recommendation-System/webApp/BRS/data/new_merged.csv', encoding="UTF-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            person = Book(
                isbn=row['ISBN'],
                title=row['Book-Title'],
                image_s=row['Image-URL-S'],
                image_m=row['Image-URL-M'],
                image_l=row['Image-URL-L'],
                genre=row['categories'].split("'")[1]
            )
            person.save()

    return HttpResponse('CSV imported successfully')
