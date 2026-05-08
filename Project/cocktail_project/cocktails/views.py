from django.http import HttpResponse


def index(request):
    return HttpResponse("Cocktail recipes app is working!")
