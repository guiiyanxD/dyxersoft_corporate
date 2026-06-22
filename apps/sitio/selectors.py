"""Consultas de solo lectura reutilizables sobre el contenido institucional.

Es la única fuente de verdad del contenido: tanto las vistas públicas
(`views.py`) como el chatbot (`apps.chatbot_empresa.services`) leen de aquí,
para no mantener el mismo contenido en dos lugares.
"""

from .models import Beneficio, Noticia, PerfilEmpresa, Proyecto, Servicio


def perfil_empresa():
    return PerfilEmpresa.objects.first() or PerfilEmpresa.objects.create()


def servicios_activos():
    return list(Servicio.objects.filter(activo=True).order_by("orden"))


def beneficios_activos():
    return list(Beneficio.objects.filter(activo=True).order_by("orden"))


def proyectos_activos_qs():
    return Proyecto.objects.filter(activo=True).order_by("orden")


def proyectos_activos():
    return list(proyectos_activos_qs())


def noticias_publicadas_qs():
    return Noticia.objects.filter(publicada=True).order_by("-fecha_publicacion")


def noticias_publicadas():
    return list(noticias_publicadas_qs())
