from django.urls import path

from . import views

urlpatterns = [
    path('', views.edicion, name='edicion'),
]