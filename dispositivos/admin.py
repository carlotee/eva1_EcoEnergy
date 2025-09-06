from django.contrib import admin
from .models import Categoria, Zona, Dispositivo, Medicion, Alerta 

admin.site.register([Categoria, Zona, Dispositivo, Medicion, Alerta])
