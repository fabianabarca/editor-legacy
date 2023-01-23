from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gtfs/', views.gtfs, name='gtfs'),
    path('acerca/', views.acerca, name='acerca'),
    path('contacto/', views.contacto, name='contacto'),
]