from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Создаёт группы"

    def handle(self, *args, **options):
        groups = ["Moderators", "Owners"]

        for name in groups:
            group, created = Group.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Группа "{name}" создана'))
            else:
                self.stdout.write(f'Группа "{name}" уже существует')
