from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncWeek
from django.db.models import Sum
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .forms import DispositivoForm
from .models import Dispositivo, Categoria, Zona, Medicion, Alerta
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

def inicio(request):
    contexto = {"nombre": "hombre araña"}
    return render(request, "dispositivos/inicio.html", contexto)

@login_required
def panel_dispositivos(request):
    dispositivos_por_categoria = Categoria.objects.annotate(conteo=Count('dispositivo'))
    dispositivos_por_zona = Zona.objects.annotate(conteo=Count('dispositivo'))

    alertas_urgentes = Alerta.objects.filter(severidad='URGENTE').count()
    alertas_medianas = Alerta.objects.filter(severidad='MEDIANA').count()

    ultimas_mediciones = Medicion.objects.order_by('-fecha')[:10]

    # Datos para la gráfica
    hoy = date.today()
    hace_7_dias = hoy - timedelta(days=7)
    hace_30_dias = hoy - timedelta(days=30)
    
    # Consumo diario
    consumo_diario = Medicion.objects.filter(fecha__date__gte=hace_7_dias)\
        .annotate(dia=TruncDay('fecha'))\
        .values('dia')\
        .annotate(consumo_total=Sum('consumo'))\
        .order_by('dia')
    
    # Consumo semanal
    consumo_semanal = Medicion.objects.filter(fecha__date__gte=hace_30_dias)\
        .annotate(semana=TruncWeek('fecha'))\
        .values('semana')\
        .annotate(consumo_total=Sum('consumo'))\
        .order_by('semana')

    return render(request, "dispositivos/panel.html", {
        "dispositivos_por_categoria": dispositivos_por_categoria,
        "dispositivos_por_zona": dispositivos_por_zona,
        "alertas_urgentes": alertas_urgentes,
        "alertas_medianas": alertas_medianas,
        "ultimas_mediciones": ultimas_mediciones,
        "consumo_diario_json": list(consumo_diario),
        "consumo_semanal_json": list(consumo_semanal)
    })

@login_required
def crear_dispositivos(request):
    if request.method == 'POST':
        form = DispositivoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_dispositivos')
    else:
        form = DispositivoForm()

    return render(request, 'dispositivos/crear.html', {'form' : form})

@login_required
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

@login_required
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

@login_required
def eliminar_dispositivo(request, dispositivo_id):
    dispositivo = get_object_or_404(Dispositivo, id=dispositivo_id)
    if request.method == 'POST':
        dispositivo.delete()
        return redirect('listar_dispositivos')
    return render(request, 'dispositivos/eliminar.html', {'dispositivo': dispositivo})

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