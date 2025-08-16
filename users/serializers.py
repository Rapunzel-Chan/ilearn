from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title", read_only=True)

    class Meta:
        model = Payment
        fields = ["course", "lesson", "payment_type",  "course_title"]


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
