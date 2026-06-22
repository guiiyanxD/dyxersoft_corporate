from django.contrib import admin

from .models import Conversacion, MensajeChat


class MensajeChatInline(admin.TabularInline):
    model = MensajeChat
    extra = 0
    readonly_fields = ["rol", "contenido", "fecha_creacion"]
    can_delete = False


@admin.register(Conversacion)
class ConversacionAdmin(admin.ModelAdmin):
    list_display = ["titulo", "session_key_corta", "cantidad_mensajes", "fecha_actualizacion"]
    readonly_fields = ["session_key", "titulo", "fecha_creacion", "fecha_actualizacion"]
    inlines = [MensajeChatInline]

    def session_key_corta(self, obj):
        return f"{obj.session_key[:10]}…"

    session_key_corta.short_description = "sesión"

    def cantidad_mensajes(self, obj):
        return obj.mensajes.count()

    cantidad_mensajes.short_description = "mensajes"

    def has_add_permission(self, request):
        return False
