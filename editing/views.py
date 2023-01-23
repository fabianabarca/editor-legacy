from django.shortcuts import render

# Create your views here.

def edicion(request):
    return render(request, 'edicion.html')
