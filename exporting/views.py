from django.shortcuts import render

# Create your views here.

def exportacion(request):
    return render(request, 'exportacion.html')