from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, 'usuarios/login.html')

def registro(request):
    return render(request, 'usuarios/registro.html')

def contrasena(request):
    return render(request, 'usuarios/contrasena.html')