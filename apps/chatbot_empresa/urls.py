from django.urls import path

from . import views

app_name = "chatbot_empresa"

urlpatterns = [
    path("", views.chat_widget_view, name="widget"),
    path("mensaje/", views.chat_mensaje_view, name="mensaje"),
    path("estado/", views.chat_estado_view, name="estado"),
]
