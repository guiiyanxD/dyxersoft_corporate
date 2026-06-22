from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("chat/", include("apps.chatbot_empresa.urls", namespace="chatbot_empresa")),
    path("", include("apps.sitio.urls", namespace="sitio")),
]

if settings.DEBUG and not getattr(settings, "RUNNING_UNDER_PYTEST", False):
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
