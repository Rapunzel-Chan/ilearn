from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.generics import CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModerator, IsOwner

# Create your views here.


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        if self.action in ["create"]:
            permission_classes = [IsAuthenticated]
        elif self.action in ["destroy"]:
            permission_classes = [IsOwner]

        elif self.action in ["update", "partial_update", "retrieve"]:
            permission_classes = [IsAuthenticated & (IsOwner | IsModerator)]
        elif self.action in ["list"]:
            permission_classes = [IsAuthenticated & IsModerator]
        else:
            permission_classes = [IsAuthenticated]
        return [perm() for perm in permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.groups.filter(name="Moderators").exists():
            return qs
        return qs.filter(owner=self.request.user)


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner | IsModerator]


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner]
