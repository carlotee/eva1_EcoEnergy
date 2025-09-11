from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django import forms
from django.contrib.auth.models import User
from .forms import RegistroEmpresaForm
# Create your views here.

def registro(request):
    return render(request, 'usuarios/registro_empresa.html')

def contrasena(request):
    return render(request, 'usuarios/contrasena.html')

def registro_empresa(request):
    if request.method == 'GET' and 'nombre' in request.GET:
        # No guardamos nada, solo redirigimos
        return redirect('panel_dispositivos')  # Cambia 'inicio' por la URL que quieras

    return render(request, 'usuarios/registro_empresa.html')

class LoginEmpresaForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

def login_empresa(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        return redirect('panel_dispositivos') 

    return render(request, 'usuarios/login_empresa.html')
