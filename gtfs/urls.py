from django.urls import path

from . import views

urlpatterns = [
    path('', views.feeds, name='feeds'),
    path('<str:version_gtfs>/', views.feed, name='feed'),
    path('<str:version_gtfs>/editar/', views.edit, name='edit'),
]