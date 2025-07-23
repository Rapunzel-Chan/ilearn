from rest_framework import serializers

from users.models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'course_title', 'sum_of_payment', 'payment_type']
