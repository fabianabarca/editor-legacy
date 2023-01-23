from django.shortcuts import render

# Create your views here.

def datos(request):
    return render(request, 'datos.html')