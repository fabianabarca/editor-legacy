from django.urls import path

from . import views

urlpatterns = [
    path('', views.edition, name='edition'),
    path('listo/', views.edited, name='edited'),
    path('agencia/', views.agency, name='agency'),
]