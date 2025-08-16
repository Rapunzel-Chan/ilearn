from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="admin@example.com", password="password")
        self.course = Course.objects.create(title="Тестирование 1", description="Основы тестирования", owner=self.user)
        self.lesson = Lesson.objects.create(
            title="Тесты. Урок 1", description="Тесты CRUD", course=self.course, owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        url = reverse("materials:lessons_create")
        data = {
            "title": "Тесты. Урок 2",
            "description": "Тесты аутентификации",
            "course": self.course.id,
            "url": "https://youtube.com/watch?v=123456",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)
        self.assertEqual(Lesson.objects.last().title, "Тесты. Урок 2")

    def test_lesson_list(self):
        url = reverse("materials:lessons_list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["title"], "Тесты. Урок 1")

    def test_lesson_retrieve(self):
        url = reverse("materials:lessons_retrieve", args=[self.lesson.id])
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Тесты. Урок 1")

    def test_lesson_update(self):
        url = reverse("materials:lessons_update", args=[self.lesson.id])
        data = {"title": "Тесты. Урок 1 (дополненный)"}
        response = self.client.patch(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Тесты. Урок 1 (дополненный)")

    def test_lesson_delete(self):
        url = reverse("materials:lessons_delete", args=[self.lesson.id])
        response = self.client.delete(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class LessonAuthTestCase(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(email="owner@example.com", password="pass")
        self.stranger = User.objects.create_user(email="stranger@example.com", password="pass")
        self.moderator = User.objects.create_user(email="moderator@example.com", password="pass", is_staff=True)

        self.course = Course.objects.create(
            title="Тестирование 2", description="Продвинутое тестирование", owner=self.owner
        )
        self.lesson = Lesson.objects.create(
            title="Тесты. Урок 3",
            description="Тестирование прав доступа",
            course=self.course,
            owner=self.owner,
            url="https://youtube.com/watch?v=abc123",
        )

    def test_stranger_cannot_update_lesson(self):
        self.client.force_authenticate(user=self.stranger)
        url = reverse("materials:lessons_update", args=[self.lesson.id])
        response = self.client.patch(url, {"title": "Взлом"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_stranger_cannot_delete_lesson(self):
        self.client.force_authenticate(user=self.stranger)
        url = reverse("materials:lessons_delete", args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_can_view_lessons(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LessonPaginationTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="admin@example.com", password="password")
        self.course = Course.objects.create(
            title="Тестирование 3", description="Лучшие практики тестирования", owner=self.user
        )

        for i in range(7):
            Lesson.objects.create(
                title=f"Урок {i+1}",
                description="Пагинация",
                course=self.course,
                owner=self.user,
                url="https://youtube.com/watch?v=pagination",
            )

        self.client.force_authenticate(user=self.user)

    def test_lessons_pagination(self):
        url = reverse("materials:lessons_list") + "?page=1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)


class LessonValidationTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="owner@example.com", password="pass")
        self.course = Course.objects.create(
            title="Тестирование 4", description="Тестирование валидаторов", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_invalid_url_rejected(self):
        url = reverse("materials:lessons_create")
        data = {
            "title": "Неверная ссылка",
            "description": "Запрещено размещать материал на сторонних или личных сайтах",
            "course": self.course.id,
            "url": "https://example.com/notyoutube",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="pass")
        self.course = Course.objects.create(
            title="Тестирование 5", description="Тестирование доп.возможностей", owner=self.user
        )

    def test_toggle_subscription(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:subscription-toggle")
        data = {"course_id": self.course.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_user_subscriptions_list(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:user-subscriptions")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_course_retrieve_includes_is_subscribed(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        url = reverse("materials:course-detail", args=[self.course.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("is_subscribed", response.data)
        self.assertTrue(response.data["is_subscribed"])
