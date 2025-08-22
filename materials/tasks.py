from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from materials.models import Course, Subscription
from users.models import User


@shared_task
def send_course_update_emails(course_id):
    course = Course.objects.get(id=course_id)
    subs = Subscription.objects.filter(course=course).select_related("user")
    for sub in subs:
        send_mail(
            subject=f"Курс '{course.title}' обновлен",
            message="Доброго времени суток, Пользователь! Ваш курс был обновлен.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[sub.user.email],
        )


@shared_task
def block_inactive_users():
    cutoff = timezone.now() - timedelta(days=30)
    users = User.objects.filter(last_login__lt=cutoff, is_active=True)
    users.update(is_active=False)
