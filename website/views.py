from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "index.html")


def acerca(request):
    return render(request, "acerca.html")


def contacto(request):
    return render(request, "contacto.html")
