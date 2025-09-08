from django.shortcuts import render, redirect
<<<<<<< HEAD
from django.contrib.auth import authenticate, login
from django import forms
# Create your views here.
def registro_empresa(request):
=======
from django.contrib.auth.models import User
from .forms import RegistroEmpresaForm
from django.contrib.auth import authenticate, login
from django import forms
# Create your views here.
def login(request):
    return render(request, 'usuarios/login.html')

def registro(request):
>>>>>>> 15999c8a5af297f7872bbe43a7e6f0f5fad87026
    return render(request, 'usuarios/registro_empresa.html')

def contraseña(request):
    return render(request, 'usuarios/contraseña.html')

<<<<<<< HEAD
=======
def registro_empresa(request):
    if request.method == 'POST':
        form = RegistroEmpresaForm(request.POST)
        if form.is_valid():
            # Crear el usuario
            User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            return render(request, 'usuarios/registro_exito.html')  # Página de confirmación
    else:
        form = RegistroEmpresaForm()
    
    return render(request, 'usuarios/registro_empresa.html', {'form': form})

>>>>>>> 15999c8a5af297f7872bbe43a7e6f0f5fad87026
class LoginEmpresaForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

def login_empresa(request):
<<<<<<< HEAD
    if request.method == 'POST':
        # Opcional: puedes capturar los datos si quieres
        username = request.POST.get('username')
        password = request.POST.get('password')

        # No autenticamos. Solo redirigimos directamente.
        return redirect('inicio')  # ← Asegúrate de tener esta vista registrada con name='inicio'

    return render(request, 'usuarios/login_empresa.html')
=======
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

>>>>>>> 15999c8a5af297f7872bbe43a7e6f0f5fad87026
