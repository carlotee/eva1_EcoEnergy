from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django import forms
# Create your views here.
def registro_empresa(request):
    return render(request, 'usuarios/registro_empresa.html')

def contraseña(request):
    return render(request, 'usuarios/contraseña.html')

class LoginEmpresaForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

def login_empresa(request):
    if request.method == 'POST':
        # Opcional: puedes capturar los datos si quieres
        username = request.POST.get('username')
        password = request.POST.get('password')

        # No autenticamos. Solo redirigimos directamente.
        return redirect('inicio')  # ← Asegúrate de tener esta vista registrada con name='inicio'

    return render(request, 'usuarios/login_empresa.html')
