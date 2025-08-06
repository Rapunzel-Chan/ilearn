# Register your models here.
from django.contrib import admin

from .models import Payment, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "phone", "town")
    search_fields = ("email", "phone", "town")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "course",
        "lesson",
        "sum_of_payment",
        "payment_type",
        "paid_date",
    )
    list_filter = (
        "payment_type",
        "paid_date",
    )
    search_fields = (
        "user__email",
        "course__title",
        "lesson__title",
    )
    ordering = ("-paid_date",)
    autocomplete_fields = ("user", "course", "lesson")
    readonly_fields = ("paid_date",)
