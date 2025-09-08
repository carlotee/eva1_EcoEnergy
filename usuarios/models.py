from django.contrib.auth.models import User
from django.db import models
from dispositivos.models import BaseModel  # si estás usando BaseModel

class Empresa(BaseModel):  # o models.Model si no quieres heredar
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
