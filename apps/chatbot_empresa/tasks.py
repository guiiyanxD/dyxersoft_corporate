from celery import shared_task
from celery.utils.log import get_task_logger

from . import services

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=2, default_retry_delay=30)
def tarea_procesar_mensaje_chat(self, mensaje_pk):
    """Genera la respuesta del asistente para un mensaje de chat (cola "ia")."""
    try:
        services.procesar_mensaje_con_llm(mensaje_pk=mensaje_pk)
    except Exception as exc:
        logger.exception("Error procesando mensaje de chat %s", mensaje_pk)
        raise self.retry(exc=exc)
