from decouple import config
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Crea el superusuario inicial si no existe (idempotente, segura para correr en cada deploy).

    Lee DJANGO_SUPERUSER_USERNAME/EMAIL/PASSWORD del entorno. Si no están
    definidas, no hace nada (no falla el deploy). Pensada para encadenarse
    en el CMD del Dockerfile junto a collectstatic/migrate.
    """

    help = "Crea el superusuario inicial a partir de variables de entorno, si todavía no existe."

    def handle(self, *args, **options):
        username = config("DJANGO_SUPERUSER_USERNAME", default="")
        email = config("DJANGO_SUPERUSER_EMAIL", default="")
        password = config("DJANGO_SUPERUSER_PASSWORD", default="")

        if not (username and email and password):
            self.stdout.write("DJANGO_SUPERUSER_* no está definido, se omite.")
            return

        Usuario = get_user_model()
        if Usuario.objects.filter(username=username).exists():
            self.stdout.write(f"El superusuario '{username}' ya existe, se omite.")
            return

        Usuario.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superusuario '{username}' creado."))
