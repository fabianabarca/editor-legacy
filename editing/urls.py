from django.urls import path

from . import views

urlpatterns = [
    path('', views.edition, name='edition'),
    path('listo/', views.edited, name='edited'),
    path('agencia/crear', views.create_agency, name='create_agency'),
    path('rutas/crear', views.create_route, name='create_route'),
    path('stop/crear', views.create_stop, name='create_stop'),
    path('agencia/lista', views.list_agency, name='list_agency'),
    path('ruta/lista', views.list_route, name='list_route'),
    path('stop/lista', views.list_stop, name='list_stop'),
    path('agencia/eliminar/<agency_id>/', views.delete_agency, name='delete_agency'),
    path('agencia/editar/<int:agency_id>/', views.edit_agency, name='edit_agency'),
    path('ruta/editar/<int:route_id>/', views.edit_route, name='edit_route'),
    path('ruta/eliminar/<route_id>/', views.delete_route, name='delete_route'),
    # path('rutas/<route_id>/', views.route, name='route')
]