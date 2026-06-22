import logging

from django.conf import settings
from django.core.mail import send_mail

from .models import MensajeContacto

logger = logging.getLogger(__name__)


def registrar_mensaje_contacto(*, nombre, email, empresa, servicio_interes, mensaje):
    """Guarda el mensaje de contacto y notifica por email best-effort (no bloqueante)."""
    contacto = MensajeContacto.objects.create(
        nombre=nombre,
        email=email,
        empresa=empresa,
        servicio_interes=servicio_interes,
        mensaje=mensaje,
    )
    try:
        send_mail(
            subject=f"Nuevo contacto desde el sitio: {nombre}",
            message=(
                f"De: {nombre} <{email}>\n"
                f"Empresa: {empresa or '-'}\n"
                f"Servicio de interés: {servicio_interes or '-'}\n\n"
                f"{mensaje}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=True,
        )
        contacto.notificado_por_email = True
        contacto.save(update_fields=["notificado_por_email"])
    except Exception:
        logger.exception("No se pudo enviar el email de notificación de contacto %s", contacto.pk)
    return contacto
