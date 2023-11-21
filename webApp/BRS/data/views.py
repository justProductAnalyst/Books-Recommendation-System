from django.http import HttpResponse


def data_home(request, isbn):
    return HttpResponse(f"<h4>Some info about book {isbn}</h4>")
