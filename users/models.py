from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Поле email обязательно")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


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
    objects = UserManager()

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
        default=timezone.now,
        verbose_name="Дата создания",
        help_text="Укажите дату создания продукта",
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
        verbose_name="Тип оплаты",
    )

    product_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="ID продукта",
        help_text="Укажите ID продукта",
    )
    price_id = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="ID стоимости продукта",
        help_text="Введите ID стоимости продукта",
    )
    session_id = models.CharField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="ID сессии",
        help_text="Укажите ID сессии",
    )
    link = models.URLField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="Ссылка для оплаты",
        help_text="Введите ссылку для оплаты",
    )

    STATUS_CHOICES = [
        ("created", "Создан"),
        ("pending", "Ожидает оплаты"),
        ("paid", "Оплачен"),
        ("canceled", "Отменен"),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="created")

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"

    def __str__(self):
        return f"Платеж {self.id} ({self.user.email}) - {self.sum_of_payment} {self.payment_type}"
