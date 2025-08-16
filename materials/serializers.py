from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import validate_youtube_url


class LessonSerializer(ModelSerializer):
    url = serializers.CharField(validators=[validate_youtube_url])

    class Meta:
        model = Lesson
        fields = "__all__"


class LessonShortSerializer(ModelSerializer):

    class Meta:
        model = Lesson
        fields = ["id", "title"]


class CourseSerializer(serializers.ModelSerializer):
    count_lesson_of_the_same_course = serializers.SerializerMethodField()
    lessons = LessonShortSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    def get_count_lesson_of_the_same_course(self, course):
        return course.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            return False
        return obj.subscriptions.filter(user=user).exists()

    class Meta:
        model = Course
        fields = (
            "title",
            "description",
            "count_lesson_of_the_same_course",
            "lessons",
            "is_subscribed",
        )


class UserSubscriptionSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source="course.title")
    course_description = serializers.CharField(source="course.description")

    class Meta:
        model = Subscription
        fields = ["course", "course_title", "course_description"]
