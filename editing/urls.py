from django.urls import path

from . import views

urlpatterns = [
    path('', views.edition, name='edition'),
    path('listo/', views.edited, name='edited'),
    path('agencia/', views.agency, name='agency'),
    path('rutas/crear', views.create_route, name='create_route'),
    path('rutas/<route_id>/', views.edit_route, name='edit_route'),
    # path('rutas/<route_id>/', views.route, name='route')
]