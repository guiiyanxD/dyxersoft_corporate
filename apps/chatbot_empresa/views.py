from django.shortcuts import render

from . import services


def chat_widget_view(request):
    """Vista inicial del widget de chat (GET) — renderiza el historial existente o vacío."""
    conversacion = services.obtener_o_crear_conversacion(request=request)
    return render(request, "chatbot_empresa/chat_widget.html", {"conversacion": conversacion})


def chat_mensaje_view(request):
    """POST del formulario de chat — guarda el mensaje y encola el procesamiento LLM."""
    conversacion = services.obtener_o_crear_conversacion(request=request)
    contenido = request.POST.get("contenido", "").strip()
    if contenido:
        services.enviar_mensaje_chat(conversacion=conversacion, contenido=contenido)
    return render(request, "chatbot_empresa/_chat_mensajes.html", {"conversacion": conversacion})


def chat_estado_view(request):
    """Polling HTMX cada 2s mientras se espera la respuesta del asistente."""
    conversacion = services.obtener_o_crear_conversacion(request=request)
    return render(request, "chatbot_empresa/_chat_mensajes.html", {"conversacion": conversacion})
