from apps.sitio import selectors as sitio_selectors

from . import llm_client
from .models import Conversacion, MensajeChat

_ROL_A_OLLAMA = {
    MensajeChat.Rol.USUARIO: "user",
    MensajeChat.Rol.ASISTENTE: "assistant",
    MensajeChat.Rol.SISTEMA: "system",
}

_PROMPT_SISTEMA_BASE = (
    "Eres el asistente virtual de Dyxersoft, una empresa de software boliviana. "
    "Respondé ÚNICAMENTE con la información institucional provista a continuación; "
    "no inventes datos, precios, plazos ni clientes que no estén en el contexto. "
    "Si te preguntan algo que no podés responder con esta información (ej. precios "
    "exactos, disponibilidad), invitá a la persona a dejar sus datos en el formulario "
    "de Contacto o a escribir por WhatsApp. Respondé en español, de forma breve, "
    "cálida y profesional."
)


def _contexto_institucional_para_prompt():
    perfil = sitio_selectors.perfil_empresa()
    servicios = sitio_selectors.servicios_activos()
    beneficios = sitio_selectors.beneficios_activos()
    proyectos = sitio_selectors.proyectos_activos()

    lineas = [
        f"Empresa: {perfil.nombre}. Tagline: {perfil.tagline}.",
        f"Ubicación: {perfil.ciudad}.",
        f"Misión/visión: {perfil.mision}",
        f"Stats: {perfil.clientes_activos}+ clientes activos, {perfil.anios_experiencia}+ años "
        f"de experiencia, {perfil.porcentaje_compromiso}% de compromiso con la calidad.",
        f"Contacto: {perfil.email_contacto} · WhatsApp {perfil.whatsapp} · "
        f"LinkedIn {perfil.linkedin_url} · Facebook {perfil.facebook_url}.",
        "Servicios: " + "; ".join(f"{s.nombre} — {s.descripcion_corta}" for s in servicios),
        "Beneficios: " + "; ".join(f"{b.titulo} — {b.descripcion}" for b in beneficios),
        "Portafolio: "
        + "; ".join(
            f"{p.nombre} ({p.cliente or 'producto propio'}) — {p.descripcion_corta}"
            for p in proyectos
        ),
    ]
    return "\n".join(lineas)


def _construir_mensajes_llm(conversacion):
    historial = conversacion.mensajes.order_by("fecha_creacion")
    contexto = _contexto_institucional_para_prompt()
    mensajes = [{"role": "system", "content": f"{_PROMPT_SISTEMA_BASE}\n\n{contexto}"}]
    mensajes += [{"role": _ROL_A_OLLAMA[m.rol], "content": m.contenido} for m in historial]
    return mensajes


def obtener_o_crear_conversacion(*, request):
    """Recupera la conversación activa de la sesión anónima, o crea una nueva."""
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key

    conversacion = (
        Conversacion.objects.filter(session_key=session_key)
        .order_by("-fecha_actualizacion")
        .first()
    )
    return conversacion or Conversacion.objects.create(session_key=session_key)


def enviar_mensaje_chat(*, conversacion, contenido):
    """Guarda el mensaje del usuario y encola el procesamiento con el LLM local."""
    mensaje = MensajeChat.objects.create(
        conversacion=conversacion, rol=MensajeChat.Rol.USUARIO, contenido=contenido
    )
    if not conversacion.titulo:
        conversacion.titulo = contenido[:60]
    conversacion.save()

    from .tasks import tarea_procesar_mensaje_chat

    tarea_procesar_mensaje_chat.delay(mensaje.pk)
    return mensaje


def procesar_mensaje_con_llm(*, mensaje_pk):
    """Genera la respuesta del asistente para el último mensaje de una conversación.

    Sin tool calling: el contenido institucional es estático y cabe completo en el
    mensaje `system`, así que basta una sola llamada a Ollama por turno. Llamada
    exclusivamente por `tasks.tarea_procesar_mensaje_chat` (cola "ia").
    """
    mensaje_usuario = MensajeChat.objects.select_related("conversacion").get(pk=mensaje_pk)
    conversacion = mensaje_usuario.conversacion

    try:
        mensajes_llm = _construir_mensajes_llm(conversacion)
        respuesta = llm_client.chat(mensajes_llm)
        contenido_final = respuesta["message"]["content"]
        MensajeChat.objects.create(
            conversacion=conversacion, rol=MensajeChat.Rol.ASISTENTE, contenido=contenido_final
        )
        conversacion.save()
    except Exception:
        MensajeChat.objects.create(
            conversacion=conversacion,
            rol=MensajeChat.Rol.ASISTENTE,
            contenido=(
                "No pude responder en este momento. Probá nuevamente en unos segundos "
                "o escribinos por WhatsApp."
            ),
        )
        conversacion.save()
        raise
