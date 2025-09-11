from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncWeek
from django.db.models import Sum
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .forms import DispositivoForm
from .models import Dispositivo
from .models import Alerta
from django.utils.timezone import now, timedelta
from .models import Dispositivo, Categoria, Zona, Medicion, Alerta
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json
from django.db.models import Q


def inicio(request):
    contexto = {"nombre": "hombre araña"}
    return render(request, "dispositivos/inicio.html", contexto)

def panel_dispositivos(request):
    print("Entrando al dashboard...")
    dispositivos_por_categoria = Categoria.objects.filter(
        estado="ACTIVO", deleted_at__isnull=True
    ).annotate(
        conteo=Count('dispositivo', filter=Q(dispositivo__estado='ACTIVO', dispositivo__deleted_at__isnull=True))
    )

    dispositivos_por_zona = Zona.objects.filter(
        estado="ACTIVO", deleted_at__isnull=True
    ).annotate(
        conteo=Count('dispositivo', filter=Q(dispositivo__estado='ACTIVO', dispositivo__deleted_at__isnull=True))
    )

    alertas_urgentes = Alerta.objects.filter(severidad='grave', deleted_at__isnull=True).count()
    alertas_medianas = Alerta.objects.filter(severidad='mediana', deleted_at__isnull=True).count()
    alertas_bajas = Alerta.objects.filter(severidad='alta', deleted_at__isnull=True).count()

    ultimas_mediciones = Medicion.objects.filter(deleted_at__isnull=True).order_by('-fecha')[:10]

    hoy = date.today()
    hace_7_dias = hoy - timedelta(days=7)
    hace_30_dias = hoy - timedelta(days=30)

    consumo_diario = Medicion.objects.filter(
        fecha__date__gte=hace_7_dias,
        deleted_at__isnull=True
    ).annotate(
        dia=TruncDay('fecha')
    ).values('dia').annotate(
        consumo_total=Sum('consumo')
    ).order_by('dia')

    consumo_semanal = Medicion.objects.filter(
        fecha__date__gte=hace_30_dias,
        deleted_at__isnull=True
    ).annotate(
        semana=TruncWeek('fecha')
    ).values('semana').annotate(
        consumo_total=Sum('consumo')
    ).order_by('semana')

    context = {
        "dispositivos_por_categoria": dispositivos_por_categoria,
        "dispositivos_por_zona": dispositivos_por_zona,
        "alertas_urgentes": alertas_urgentes,
        "alertas_medianas": alertas_medianas,
        "alertas_bajas": alertas_bajas,
        "ultimas_mediciones": ultimas_mediciones,
        "consumo_diario_json": json.dumps(list(consumo_diario), default=str),
        "consumo_semanal_json": json.dumps(list(consumo_semanal), default=str),
    }
    return render(request, "dispositivos/panel.html", context)

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
    categoria_seleccionada = request.GET.get('categoria')

    if categoria_seleccionada:
        dispositivos = Dispositivo.objects.filter(categoria_id=categoria_seleccionada)
    else:
        dispositivos = Dispositivo.objects.all()

    categorias = Categoria.objects.all()

    return render(request, "dispositivos/listar_dispositivos.html", {
        "dispositivos": dispositivos,
        "categorias": categorias,
        "categoria_seleccionada": int(categoria_seleccionada) if categoria_seleccionada else None
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



def alerta_semanal_view(request):
    fecha_fin = now()
    fecha_inicio = fecha_fin - timedelta(days=7)

    alertas_semana = Alerta.objects.filter(fecha__range=(fecha_inicio, fecha_fin)).select_related('dispositivo', 'dispositivo__categoria', 'dispositivo__zona').order_by('-fecha')

    context = {
        'alertas_semana': alertas_semana,
    }

    return render(request, 'dispositivos/alerta_semanal.html', context)

def generar_y_enviar_alertas(request):
    mediciones_recientes = Medicion.objects.filter(fecha__date=date.today())
    
    for medicion in mediciones_recientes:
        if medicion.consumo > medicion.dispositivo.consumo_maximo:
            # Crea la alerta en la base de datos
            alerta = Alerta.objects.create(
                dispositivo=medicion.dispositivo,
                severidad='URGENTE',
                descripcion=f"Consumo superado: {medicion.consumo} kWh > {medicion.dispositivo.consumo_maximo} kWh"
            )

            # Envía el correo electrónico al usuario asociado
            empresa_usuario = medicion.dispositivo.zona.empresa.usuario
            email_usuario = empresa_usuario.email
            
            subject = f"Alerta de alto consumo: {medicion.dispositivo.nombre}"
            message = render_to_string('email/alerta_email.html', {
                'alerta': alerta,
                'dispositivo': medicion.dispositivo,
                'medicion': medicion
            })

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email_usuario],
                fail_silently=False,
            )
    
def listado_mediciones(request):
    mediciones = Medicion.objects.select_related('dispositivo').order_by('-fecha')
    paginador = Paginator(mediciones, 50)  # Máximo 50 por página

    pagina_num = request.GET.get('page')
    pagina_obj = paginador.get_page(pagina_num)

    return render(request, 'dispositivos/mediciones.html', {'pagina_obj': pagina_obj})

def detalle_dispositivo(request, pk):
    dispositivo = get_object_or_404(Dispositivo, pk=pk)
    return render(request, 'dispositivos/detalle_dispositivo.html', {'dispositivo': dispositivo})

