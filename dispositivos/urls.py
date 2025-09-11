from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
    path('panel/', views.panel_dispositivos, name='panel_dispositivos'),
    path('dispositivos/', views.listar_dispositivos, name='listar_dispositivos'),
    path('dispositivos/crear/', views.crear_dispositivos, name='crear_dispositivos'),
    path('dispositivos/editar/<int:dispositivo_id>/', views.editar_dispositivo, name='editar_dispositivo'),
    path('dispositivos/eliminar/<int:dispositivo_id>/', views.eliminar_dispositivo, name='eliminar_dispositivo'),
]