from django.contrib import admin

from .models import Beneficio, MensajeContacto, Noticia, PerfilEmpresa, Proyecto, Servicio


@admin.register(PerfilEmpresa)
class PerfilEmpresaAdmin(admin.ModelAdmin):
    list_display = ["nombre", "tagline", "email_contacto"]

    def has_add_permission(self, request):
        return not PerfilEmpresa.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ["nombre", "slug", "orden", "activo"]
    list_editable = ["orden", "activo"]
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Beneficio)
class BeneficioAdmin(admin.ModelAdmin):
    list_display = ["titulo", "orden", "activo"]
    list_editable = ["orden", "activo"]


@admin.register(Proyecto)
class ProyectoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "cliente", "slug_demo", "orden", "activo"]
    list_editable = ["orden", "activo"]
    prepopulated_fields = {"slug": ("nombre",)}


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ["titulo", "publicada", "fecha_publicacion", "fecha_creacion"]
    list_editable = ["publicada"]
    prepopulated_fields = {"slug": ("titulo",)}
    date_hierarchy = "fecha_creacion"


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ["nombre", "email", "servicio_interes", "fecha_creacion", "notificado_por_email"]
    list_filter = ["servicio_interes", "notificado_por_email"]
    readonly_fields = [f.name for f in MensajeContacto._meta.fields]

    def has_add_permission(self, request):
        return False
