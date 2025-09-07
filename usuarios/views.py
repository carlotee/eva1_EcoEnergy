from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django import forms
# Create your views here.
def registro(request):
    return render(request, 'usuarios/registro_empresa.html')

def contraseña(request):
    return render(request, 'usuarios/contraseña.html')

class LoginEmpresaForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

def login_empresa(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Cambia 'home' por la vista a la que deseas redirigir
        else:
            error_message = "Credenciales incorrectas. Inténtalo de nuevo."

    return render(request, 'usuarios/login_empresa.html', {'error_message': error_message})
