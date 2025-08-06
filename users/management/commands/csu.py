from django.conf import settings
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        self.stdout.write(f"ADMIN_PASSWORD from settings: {settings.ADMIN_PASSWORD}")
        user, created = User.objects.get_or_create(
            email="admin@example.com", defaults={"is_active": True, "is_staff": True, "is_superuser": True}
        )
        if created:
            if not settings.ADMIN_PASSWORD:
                self.stdout.write(self.style.ERROR("ADMIN_PASSWORD is not set!"))
                return
            user.set_password(settings.ADMIN_PASSWORD)
            user.save()
            self.stdout.write(self.style.SUCCESS("Superuser created"))
        else:
            self.stdout.write("Admin user already exists")
