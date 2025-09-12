"""
URL configuration for monitoreo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from usuarios import views as usuario_views
from django.urls import path, include
from dispositivos.views import inicio
from dispositivos import views
from usuarios import views as usuarios_views
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inicio/', inicio, name='inicio'),
    path('panel/', views.panel_dispositivos, name='panel_dispositivos'),
    path('dispositivos/crear/', views.crear_dispositivos, name='crear_dispositivos'),
    path('dispositivos/listar_dispositivos/', views.listar_dispositivos, name='listar_dispositivos'),
    path('dispositivos/eliminar/<int:dispositivo_id>/', views.eliminar_dispositivo, name='eliminar_dispositivo'),
    path('dispositivos/alerta_semanal/<int:dispositivo_id>/', views.alerta_semanal, name='alerta_semanal'),
    path('usuarios/contrasena/', usuarios_views.contrasena, name='contrasena'),
    path('usuarios/registro/', usuario_views.registro_empresa, name='registro_empresa'),
    path('usuarios/login_empresa/', usuario_views.login_empresa, name='login_empresa'),
    path('editar/<int:dispositivo_id>/', views.editar_dispositivo, name='editar_dispositivo'),
    path('mediciones/', views.listado_mediciones, name='listado_mediciones'),
    path('dispositivos/<int:pk>/', views.detalle_dispositivo, name='detalle_dispositivo'),
    path('dispositivos/alertas/', views.alertas_todas, name='alertas_todas'),
    path('alerta/nueva/', views.crear_alerta, name='crear_alerta'),

    ]