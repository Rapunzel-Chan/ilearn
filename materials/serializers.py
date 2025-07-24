from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    count_lesson_of_the_same_course = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)

    def get_count_lesson_of_the_same_course(self, course):
        return course.lessons.count()

    def get_lessons(self, course):
        return [lesson.title for lesson in Lesson.objects.filter(course=course)]

    class Meta:
        model = Course
        fields = (
            "title",
            "description",
            "count_lesson_of_the_same_course",
            "lessons",
        )


# class CourseDetailSerializer(ModelSerializer):
#     count_lesson_of_same_course =
#     class Meta:
#         model = Course
#         fields = ("title", "description", "count_lesson_of_same_course",)
