from django_filters import rest_framework as filters

from users.models import Payment


class PaymentFilter(filters.FilterSet):
    course = filters.NumberFilter(field_name="course")
    lesson = filters.NumberFilter(field_name="lesson")
    payment_type = filters.ChoiceFilter(field_name="payment_type", choices=Payment.TYPE_CHOICES)

    class Meta:
        model = Payment
        fields = ["course", "lesson", "payment_type"]
