from django.urls import path

from . import views

app_name = "sitio"

urlpatterns = [
    path("", views.inicio_view, name="inicio"),
    path("servicios/", views.servicios_view, name="servicios"),
    path("nosotros/", views.nosotros_view, name="nosotros"),
    path("portafolio/", views.portafolio_view, name="portafolio"),
    path("portafolio/<slug:slug>/", views.proyecto_detalle_view, name="proyecto_detalle"),
    path("contacto/", views.contacto_view, name="contacto"),
    path("boletin/", views.boletin_lista_view, name="boletin_lista"),
    path("boletin/<slug:slug>/", views.boletin_detalle_view, name="boletin_detalle"),
]
