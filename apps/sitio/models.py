from django.db import models
from django.urls import reverse


class PerfilEmpresa(models.Model):
    """Singleton con la información institucional de Dyxersoft."""

    nombre = models.CharField(max_length=100, default="Dyxersoft")
    tagline = models.CharField(
        max_length=200, default="Soluciones SaaS, IA y Gestión Inteligente de Incidencias"
    )
    mision = models.TextField(
        "misión y visión",
        default=(
            "Somos un equipo multidisciplinario de desarrolladores, ingenieros de datos, "
            "diseñadores y consultores tecnológicos con base en Santa Cruz de la Sierra, "
            "Bolivia. Nuestra visión es clara: ayudar a empresas latinoamericanas a escalar "
            "con tecnología de clase mundial. Combinamos experiencia local con estándares "
            "globales para entregar soluciones que realmente funcionan. Desde plataformas "
            "SaaS hasta proyectos de inteligencia artificial, trabajamos con metodologías "
            "ágiles, soporte continuo y un compromiso real con el éxito de nuestros clientes."
        ),
    )
    ciudad = models.CharField(max_length=100, default="Santa Cruz de la Sierra, Bolivia")
    anios_experiencia = models.PositiveIntegerField("años de experiencia", default=5)
    clientes_activos = models.PositiveIntegerField("clientes activos", default=30)
    porcentaje_compromiso = models.PositiveIntegerField("% compromiso con calidad", default=100)
    email_contacto = models.EmailField(default="contacto@dyxersoft.com")
    whatsapp = models.CharField(max_length=30, default="+591 620694477")
    linkedin_url = models.URLField(default="https://linkedin.com/company/dyxersoft")
    facebook_url = models.URLField(default="https://facebook.com/dyxersoft")

    class Meta:
        verbose_name = "perfil de la empresa"
        verbose_name_plural = "perfil de la empresa"

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True)
    descripcion_corta = models.CharField(max_length=300)
    icono = models.CharField(
        "clase de icono (Bootstrap Icons)",
        max_length=50,
        blank=True,
        help_text="Ej: bi-cloud, bi-cpu",
    )
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "servicio"
        verbose_name_plural = "servicios"
        ordering = ["orden", "nombre"]

    def __str__(self):
        return self.nombre


class Beneficio(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300)
    icono = models.CharField(max_length=50, blank=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "beneficio"
        verbose_name_plural = "beneficios"
        ordering = ["orden", "titulo"]

    def __str__(self):
        return self.titulo


class Proyecto(models.Model):
    """Entrada del Portafolio (ej: PIGIM, Sistema de Becas/DUBSS)."""

    nombre = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True)
    descripcion_corta = models.CharField(max_length=300)
    descripcion_larga = models.TextField(blank=True)
    cliente = models.CharField(max_length=150, blank=True, help_text="Ej: DUBSS - UAGRM")
    imagen = models.ImageField(upload_to="portafolio/", blank=True, null=True)
    servicio_relacionado = models.ForeignKey(
        Servicio, on_delete=models.SET_NULL, null=True, blank=True, related_name="proyectos"
    )
    slug_demo = models.SlugField(
        "slug para 'Solicitar demo'",
        max_length=160,
        help_text="Valor usado en ?servicio=<slug_demo> al precargar el formulario de contacto.",
    )
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = "proyecto"
        verbose_name_plural = "proyectos (portafolio)"
        ordering = ["orden", "-id"]

    def __str__(self):
        return self.nombre

    def get_absolute_url(self):
        return reverse("sitio:proyecto_detalle", kwargs={"slug": self.slug})

    def url_solicitar_demo(self):
        return f"{reverse('sitio:contacto')}?servicio={self.slug_demo}"


class Noticia(models.Model):
    """Entrada del boletín. Gestionada 100% desde Django Admin estándar."""

    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=210, unique=True)
    resumen = models.CharField(max_length=300)
    contenido = models.TextField()
    imagen = models.ImageField(upload_to="boletin/", blank=True, null=True)
    publicada = models.BooleanField(default=False)
    fecha_publicacion = models.DateTimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "noticia"
        verbose_name_plural = "noticias (boletín)"
        ordering = ["-fecha_publicacion", "-fecha_creacion"]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("sitio:boletin_detalle", kwargs={"slug": self.slug})


class MensajeContacto(models.Model):
    """Buzón de mensajes enviados desde el formulario de Contacto. Solo lectura desde Admin."""

    nombre = models.CharField(max_length=150)
    email = models.EmailField()
    empresa = models.CharField(max_length=150, blank=True)
    servicio_interes = models.CharField(
        "servicio de interés",
        max_length=60,
        blank=True,
        help_text="Slug de Servicio o Proyecto.slug_demo elegido en el formulario.",
    )
    mensaje = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    notificado_por_email = models.BooleanField(default=False)

    class Meta:
        verbose_name = "mensaje de contacto"
        verbose_name_plural = "mensajes de contacto"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return f"{self.nombre} <{self.email}>"
