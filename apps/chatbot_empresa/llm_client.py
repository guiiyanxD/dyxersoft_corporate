"""Cliente delgado sobre Ollama (LLM local). Sin lógica de negocio — solo I/O.

Lee `OLLAMA_BASE_URL`/`OLLAMA_MODEL` de settings. Quien procese esto debe ser un
worker con acceso de red al contenedor "ollama" (cola Celery "ia").
"""

import ollama
from django.conf import settings


def chat(mensajes):
    """Envía una conversación al modelo local y devuelve la respuesta de Ollama."""
    cliente = ollama.Client(host=settings.OLLAMA_BASE_URL)
    return cliente.chat(model=settings.OLLAMA_MODEL, messages=mensajes)
