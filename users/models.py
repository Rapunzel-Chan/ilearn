from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

# Create your models here.


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
        help_text="Укажите электронный адрес",
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите номер телефона",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="Аватар",
        blank=True,
        null=True,
        help_text="Загрузите свой аватар",
    )
    town = models.CharField(
        max_length=50,
        verbose_name="Город",
        blank=True,
        null=True,
        help_text="Укажите город",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="payments",
        verbose_name="Пользователь",
        help_text="Укажите Пользователя",
    )

    paid_date = models.DateTimeField(
        default=timezone.now, verbose_name="Дата создания", help_text="Введите дату создания продукта"
    )
    course = models.ForeignKey("materials.Course", on_delete=models.SET_NULL, null=True, blank=True)
    lesson = models.ForeignKey("materials.Lesson", on_delete=models.SET_NULL, null=True, blank=True)
    sum_of_payment = models.DecimalField(max_digits=10, decimal_places=2)

    TYPE_CHOICES = [
        ("cash", "Наличный расчет"),
        ("cashless", "Безналичный расчет"),
    ]

    payment_type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        # default='created',
        verbose_name="Тип оплаты",
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"
