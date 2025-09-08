from django.shortcuts import get_object_or_404, render, redirect
from .forms import DispositivoForm
from .models import Dispositivo, Categoria, Zona, Medicion, Alerta
from django.db.models import Count, Q


def inicio(request):
    contexto = {"nombre": "hombre araña"}
    return render(request, "dispositivos/inicio.html", contexto)


def panel_dispositivos(request):
    # Conteo de dispositivos por categoría
    dispositivos_por_categoria = Categoria.objects.annotate(
        conteo=Count('dispositivo__id')
    ).values('nombre', 'conteo')

    # Conteo de dispositivos por zona
    dispositivos_por_zona = Zona.objects.annotate(
        conteo=Count('dispositivo__id')
    ).values('nombre', 'conteo')

    # Conteo de alertas de la semana por severidad
    alertas_graves = Alerta.objects.filter(
        severidad=Alerta.SEVERIDAD_GRAVE
    ).count()

    alertas_altas = Alerta.objects.filter(
        severidad=Alerta.SEVERIDAD_ALTA
    ).count()

    alertas_medianas = Alerta.objects.filter(
        severidad=Alerta.SEVERIDAD_MEDIANA
    ).count()

    # Últimas 10 mediciones ordenadas por fecha
    ultimas_mediciones = Medicion.objects.select_related(
        'dispositivo'
    ).order_by('-fecha')[:10]

    contexto = {
        "dispositivos_por_categoria": dispositivos_por_categoria,
        "dispositivos_por_zona": dispositivos_por_zona,
        "alertas_graves": alertas_graves,
        "alertas_altas": alertas_altas,
        "alertas_medianas": alertas_medianas,
        "ultimas_mediciones": ultimas_mediciones,
    }

    return render(request, "dispositivos/panel.html", contexto)


def crear_dispositivos(request):
    if request.method == 'POST':
        form = DispositivoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_dispositivos')
    else:
        form = DispositivoForm()

    return render(request, 'dispositivos/crear.html', {'form': form})


def listar_dispositivos(request):
    # Obtiene todos los dispositivos por defecto
    dispositivos = Dispositivo.objects.all()
    # Obtiene todas las categorías para el filtro
    categorias = Categoria.objects.all()

    # Verifica si se envió un filtro de categoría en la URL
    categoria_id = request.GET.get('categoria')

    if categoria_id:
        # Si hay un ID de categoría, filtra los dispositivos
        dispositivos = dispositivos.filter(categoria_id=categoria_id)

    # Puedes agregar orden por nombre para mantener el orden
    dispositivos = dispositivos.order_by('nombre')

    return render(request, "dispositivos/listar_dispositivos.html", {
        "dispositivos": dispositivos,
        "categorias": categorias,
        "categoria_seleccionada": int(categoria_id) if categoria_id else None
    })


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
