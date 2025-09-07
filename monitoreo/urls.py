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
from django.urls import path
from dispositivos.views import inicio
from dispositivos import views
from usuarios import views as usuarios_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio),
    path('panel/', views.panel_dispositivos, name='panel_dispositivos'),
    path('dispositivos/crear/', views.crear_dispositivos, name='crear_dispositivos'),
    path('dispositivos/listar_dispositivos/', views.listar_dispositivos, name='listar_dispositivos'),
    path('dispositivos/eliminar/<int:dispositivo_id>/', views.eliminar_dispositivo, name='eliminar_dispositivo'),
    path('usuarios/login_empresa/',usuarios_views.login_empresa, name='login_empresa'),
    path('usuarios/registro_empresa/', usuarios_views.registro_empresa, name='registro_empresa'),
]
