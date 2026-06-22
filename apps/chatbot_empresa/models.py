from django.db import models


class Conversacion(models.Model):
    """Conversación de chat público. Identidad anónima vía session_key (sin FK a usuario)."""

    session_key = models.CharField(max_length=40, db_index=True)
    titulo = models.CharField(max_length=200, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "conversación del chatbot"
        verbose_name_plural = "conversaciones del chatbot"
        ordering = ["-fecha_actualizacion"]

    def __str__(self):
        return self.titulo or f"Conversación #{self.pk}"


class MensajeChat(models.Model):
    class Rol(models.TextChoices):
        USUARIO = "USUARIO", "Usuario"
        ASISTENTE = "ASISTENTE", "Asistente"
        SISTEMA = "SISTEMA", "Sistema"

    conversacion = models.ForeignKey(
        Conversacion, on_delete=models.CASCADE, related_name="mensajes"
    )
    rol = models.CharField(max_length=20, choices=Rol.choices)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "mensaje de chat"
        verbose_name_plural = "mensajes de chat"
        ordering = ["fecha_creacion"]

    def __str__(self):
        return f"{self.get_rol_display()}: {self.contenido[:50]}"
