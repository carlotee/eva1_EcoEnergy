from django.shortcuts import get_object_or_404
from .models import Medicion
from django.shortcuts import render, redirect
from .forms import DispositivoForm
from .models import Dispositivo
from .models import Alerta
from django.utils.timezone import now, timedelta
# Create your views here.

def inicio(request):
    contexto = {"nombre": "hombre araña"}
    return render(request,"dispositivos/inicio.html", contexto)

def panel_dispositivos(request):
    dispositivos = [
        {"nombre": "Sensor Temperatura", "consumo": 50},
        {"nombre": "Medidor Solar", "consumo": 120},
        {"nombre": "Sensor Movimiento", "consumo": 30},
        {"nombre": "Calefactor", "consumo": 200},
    ]

    consumo_maximo = 100

    return render(request, "dispositivos/panel.html", {
        "dispositivos": dispositivos,
        "consumo_maximo": consumo_maximo
    })

def crear_dispositivos(request):
    if request.method == 'POST':
        form = DispositivoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_dispositivos')
    else:
        form = DispositivoForm()

    return render(request, 'dispositivos/crear.html', {'form' : form})


def listar_dispositivos(request):
    dispositivos = Dispositivo.objects.all()
    return render(request, "dispositivos/listar_dispositivos.html", {"dispositivos": dispositivos})

def editar_dispositivo(request, dispositivo_id):
    dispositivo = get_object_or_404(Dispositivo, id=dispositivo_id)
    if request.method == 'POST':
        form = DispositivoForm(request.POST, instance=dispositivo)
        if form.is_valid():
            form.save()
            return redirect('listar_dispositivos')
    else:
        form = DispositivoForm(instance=dispositivo)
    return render(request, 'dispositivos/editar.html', {'form': form})

def eliminar_dispositivo(request, dispositivo_id):
    dispositivo = get_object_or_404(Dispositivo, id=dispositivo_id)
    if request.method == 'POST':
        dispositivo.delete()
        return redirect('listar_dispositivos')
    return render(request, 'dispositivos/eliminar.html', {'dispositivo': dispositivo})


def alerta_semanal_view(request):
    fecha_fin = now()
    fecha_inicio = fecha_fin - timedelta(days=7)

    alertas_semana = Alerta.objects.filter(fecha__range=(fecha_inicio, fecha_fin)).select_related('dispositivo', 'dispositivo__categoria', 'dispositivo__zona').order_by('-fecha')

    context = {
        'alertas_semana': alertas_semana,
    }

    return render(request, 'dispositivos/alerta_semanal.html', context)
