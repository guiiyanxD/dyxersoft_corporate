from django.core.management.base import BaseCommand

from apps.sitio.models import Beneficio, PerfilEmpresa, Proyecto, Servicio

SERVICIOS = [
    ("Desarrollo SaaS", "saas", "bi-cloud-fill",
     "Plataformas de software como servicio escalables y multi-tenant."),
    ("Desarrollo web y móvil", "web-movil", "bi-phone-fill",
     "Aplicaciones web y móviles a medida, de punta a punta."),
    ("Software personalizado", "software-personalizado", "bi-gear-fill",
     "Sistemas a medida para procesos específicos de tu negocio."),
    ("Ingeniería de datos", "ingenieria-datos", "bi-diagram-3-fill",
     "Pipelines y arquitecturas de datos robustas y escalables."),
    ("Business Intelligence", "business-intelligence", "bi-bar-chart-fill",
     "Análisis de datos para la toma de decisiones estratégicas."),
    ("Dashboards ejecutivos", "dashboards-ejecutivos", "bi-speedometer2",
     "Visualización de KPIs en tiempo real para la dirección."),
    ("Automatización de procesos", "automatizacion-procesos", "bi-arrow-repeat",
     "Eliminación de tareas manuales repetitivas con software."),
    ("Integración de sistemas", "integracion-sistemas", "bi-plug-fill",
     "Conectamos tus plataformas existentes entre sí."),
    ("Inteligencia artificial", "inteligencia-artificial", "bi-cpu-fill",
     "Soluciones de IA aplicadas a problemas reales del negocio."),
    ("QA Testing", "qa-testing", "bi-check2-square",
     "Aseguramiento de calidad de software con pruebas exhaustivas."),
    ("Modernización de sistemas legacy", "modernizacion-legacy", "bi-arrow-up-circle-fill",
     "Migración y actualización de sistemas antiguos."),
    ("Consultoría tecnológica", "consultoria-tecnologica", "bi-lightbulb-fill",
     "Asesoría estratégica en adopción de tecnología."),
]

BENEFICIOS = [
    ("Experiencia local, estándares globales", "bi-globe2",
     "Conocemos el mercado boliviano y aplicamos buenas prácticas internacionales."),
    ("Equipo multidisciplinario", "bi-people-fill",
     "Desarrolladores, ingenieros de datos, diseñadores y consultores en un solo equipo."),
    ("Presencia en Bolivia", "bi-geo-alt-fill",
     "Atención cercana, en el mismo huso horario y cultura."),
    ("Soporte continuo", "bi-headset",
     "Acompañamiento más allá de la entrega del proyecto."),
    ("Metodología ágil", "bi-rocket-takeoff-fill",
     "Entregas iterativas con visibilidad constante del avance."),
    ("Seguridad y confiabilidad", "bi-shield-check",
     "Buenas prácticas de seguridad en cada solución que entregamos."),
]

PROYECTOS = [
    {
        "nombre": "PIGIM",
        "slug": "pigim",
        "slug_demo": "demo-pigim",
        "descripcion_corta": "Plataforma Inteligente de Gestión de Incidencias.",
        "descripcion_larga": (
            "Centraliza, prioriza y resuelve incidencias empresariales con métricas en "
            "tiempo real."
        ),
        "cliente": "",
    },
    {
        "nombre": "Sistema de Gestión de Becas Universitarias",
        "slug": "sistema-becas-dubss",
        "slug_demo": "demo-becas",
        "descripcion_corta": (
            "Plataforma de convocatorias de becas: postulación, validación documental, "
            "procesamiento socioeconómico y ranking automatizado."
        ),
        "descripcion_larga": "",
        "cliente": "DUBSS - UAGRM",
    },
]


class Command(BaseCommand):
    help = "Carga el contenido institucional inicial de Dyxersoft (idempotente)."

    def handle(self, *args, **options):
        self._cargar_perfil()
        self._cargar_servicios()
        self._cargar_beneficios()
        self._cargar_proyectos()
        self.stdout.write(self.style.SUCCESS("\nContenido institucional cargado."))

    def _cargar_perfil(self):
        _, created = PerfilEmpresa.objects.get_or_create(pk=1)
        estado = "[creado] " if created else "[omitido]"
        self.stdout.write(f"  {estado} PerfilEmpresa")

    def _cargar_servicios(self):
        for orden, (nombre, slug, icono, descripcion) in enumerate(SERVICIOS):
            _, created = Servicio.objects.get_or_create(
                slug=slug,
                defaults={
                    "nombre": nombre,
                    "icono": icono,
                    "descripcion_corta": descripcion,
                    "orden": orden,
                },
            )
            estado = "[creado] " if created else "[omitido]"
            self.stdout.write(f"  {estado} Servicio: {nombre}")

    def _cargar_beneficios(self):
        for orden, (titulo, icono, descripcion) in enumerate(BENEFICIOS):
            _, created = Beneficio.objects.get_or_create(
                titulo=titulo,
                defaults={"icono": icono, "descripcion": descripcion, "orden": orden},
            )
            estado = "[creado] " if created else "[omitido]"
            self.stdout.write(f"  {estado} Beneficio: {titulo}")

    def _cargar_proyectos(self):
        for orden, datos in enumerate(PROYECTOS):
            _, created = Proyecto.objects.get_or_create(
                slug=datos["slug"],
                defaults={
                    "nombre": datos["nombre"],
                    "slug_demo": datos["slug_demo"],
                    "descripcion_corta": datos["descripcion_corta"],
                    "descripcion_larga": datos["descripcion_larga"],
                    "cliente": datos["cliente"],
                    "orden": orden,
                },
            )
            estado = "[creado] " if created else "[omitido]"
            self.stdout.write(f"  {estado} Proyecto: {datos['nombre']}")
