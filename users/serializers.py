from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = Payment
        fields = ["course", "lesson", "payment_type", "course_title"]


class PaymentCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = ["course", "lesson", "sum_of_payment", "payment_type"]


class PaymentDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "course",
            "lesson",
            "sum_of_payment",
            "payment_type",
            "status",
            "checkout_url",
            "stripe_session_id",
            "paid_date",
        ]
        depth = 1


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "avatar", "town"]


class UserPrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]
