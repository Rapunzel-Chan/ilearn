from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from materials.models import Course, Lesson
from users.models import User


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
