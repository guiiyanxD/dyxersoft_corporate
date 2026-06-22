from django.shortcuts import get_object_or_404, render

from . import selectors, services
from .forms import ContactoForm


def inicio_view(request):
    contexto = {
        "perfil": selectors.perfil_empresa(),
        "servicios": selectors.servicios_activos()[:6],
        "beneficios": selectors.beneficios_activos(),
        "proyectos": selectors.proyectos_activos()[:2],
        "noticias": selectors.noticias_publicadas()[:3],
    }
    return render(request, "sitio/inicio.html", contexto)


def servicios_view(request):
    return render(request, "sitio/servicios.html", {"servicios": selectors.servicios_activos()})


def nosotros_view(request):
    contexto = {
        "perfil": selectors.perfil_empresa(),
        "beneficios": selectors.beneficios_activos(),
    }
    return render(request, "sitio/nosotros.html", contexto)


def portafolio_view(request):
    return render(request, "sitio/portafolio.html", {"proyectos": selectors.proyectos_activos()})


def proyecto_detalle_view(request, slug):
    proyecto = get_object_or_404(selectors.proyectos_activos_qs(), slug=slug)
    return render(request, "sitio/proyecto_detalle.html", {"proyecto": proyecto})


def contacto_view(request):
    if request.method == "POST":
        form = ContactoForm(request.POST)
        if form.is_valid():
            services.registrar_mensaje_contacto(**form.cleaned_data)
            return render(request, "sitio/contacto_enviado.html")
    else:
        form = ContactoForm(initial={"servicio_interes": request.GET.get("servicio", "")})
    return render(request, "sitio/contacto.html", {"form": form})


def boletin_lista_view(request):
    return render(request, "sitio/boletin_lista.html", {"noticias": selectors.noticias_publicadas()})


def boletin_detalle_view(request, slug):
    noticia = get_object_or_404(selectors.noticias_publicadas_qs(), slug=slug)
    return render(request, "sitio/boletin_detalle.html", {"noticia": noticia})
