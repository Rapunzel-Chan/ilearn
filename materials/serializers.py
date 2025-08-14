from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson
from materials.validators import validate_youtube_url


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class LessonShortSerializer(ModelSerializer):
    url = serializers.CharField(validators=[validate_youtube_url])

    class Meta:
        model = Lesson
        fields = ["id", "title"]


class CourseSerializer(serializers.ModelSerializer):
    count_lesson_of_the_same_course = serializers.SerializerMethodField()
    lessons = LessonShortSerializer(many=True, read_only=True)

    def get_count_lesson_of_the_same_course(self, course):
        return course.lessons.count()

    class Meta:
        model = Course
        fields = (
            "title",
            "description",
            "count_lesson_of_the_same_course",
            "lessons",
        )
