from django.conf import settings
from django.db import models


# Create your models here.
class Course(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание курса",
        blank=True,
        null=True,
    )
    preview_image = models.ImageField(
        upload_to="materials/preview_course_image/",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите превью курса",
    )
    owner = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Владелец")
    updated_at = models.DateTimeField(
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["title"]

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        verbose_name="Описание",
        help_text="Введите описание урока",
        blank=True,
        null=True,
    )
    photo = models.ImageField(
        upload_to="materials/preview_lesson_image/",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите превью урока",
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс", help_text="Выберите курс"
    )
    url = models.URLField(
        verbose_name="Ссылка на видео",
        help_text="Укажите ссылку на видео",
        blank=True,
        null=True,
    )
    owner = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Владелец",
        help_text="Укажите владельца",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["course", "title"]

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions", verbose_name="Пользователь"
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="subscriptions", verbose_name="Курс")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "course")
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        ordering = ["-created_at"]
