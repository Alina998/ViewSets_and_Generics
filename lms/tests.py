from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from lms.models import Course, Lesson
from users.models import User


class LmsTestCase(APITestCase):
    """Тест моделей Course и Lesson"""

    def setUp(self) -> None:
        """Создается тестовый пользователь"""
        self.user = User.objects.create(
            email="test@mail.ru",
        )
        # self.user.set_password("test_pass_1")
        # self.user.save()
        # self.client.force_authenticate(user=self.user)

        """Создается тестовый курс"""
        self.course = Course.objects.create(
            name="test course", description="test course description", owner=self.user
        )

        """Создается тестовый урок"""
        self.lesson = Lesson.objects.create(
            name="test lesson",
            description="test lesson description",
            video_link="https://www.youtube.com/",
            course=self.course,
            owner=self.user,
        )

        self.client.force_authenticate(user=self.user)

    def test_list_lesson(self):
        """Тест для получения списка уроков"""

        url = reverse("lms:lesson-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        print(response.json())

        self.assertEqual(
            Lesson.objects.get(pk=self.lesson.pk).name,
            response.json().get("results")[0].get("name"),
        )

    def test_retrieve_lesson(self):
        """Тест для просмотра урока"""
        # response = self.client.get(f"/lessons/{self.lesson.pk}/")
        url = reverse("lms:lesson-detail", args=(self.lesson.pk,))
        response = self.client.get(url)

        print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        response = response.json()

        self.assertEqual(response.get("name"), "test lesson")
        self.assertEqual(response.get("preview"), None)
        self.assertEqual(response.get("description"), "test lesson description")
        self.assertEqual(response.get("video_link"), "https://www.youtube.com/")
        self.assertEqual(response.get("course"), self.course.pk)
        self.assertEqual(response.get("owner"), self.user.pk)

    def test_create_lesson(self):
        """Тест для создания урока"""
        data = {
            "name": "test lesson 2",
            "description": "description 2",
            "video_link": "https://www.youtube.com/",
            "course": self.course.pk,
            "owner": self.user.pk,
        }

        lesson_create_url = reverse("lms:lesson-create")
        response = self.client.post(lesson_create_url, data=data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        print(response.json())

        self.assertEqual(response.json().get("name"), data.get("name"))

        self.assertTrue(Lesson.objects.get(pk=self.lesson.pk).name, data.get("name"))

    def test_update_lesson(self):
        """Тест для обновления урока"""
        data = {
            "name": "updated lesson",
            "description": "updated description",
            "video_link": "https://www.youtube.com/",
            "course": self.course.pk,
        }

        url = reverse("lms:lesson-update", args=(self.lesson.pk,))
        response = self.client.put(url, data=data)

        print(response.json())

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        response = response.json()

        self.assertEqual(response.get("name"), "updated lesson")
        self.assertEqual(response.get("description"), "updated description")
        self.assertEqual(response.get("course"), self.course.pk)
        self.assertEqual(response.get("owner"), self.user.pk)

    def test_delete_lesson(self):
        """Тест для удаления урока"""
        lesson_delete_url = reverse("lms:lesson-delete", args=(self.lesson.pk,))
        response = self.client.delete(lesson_delete_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Lesson.objects.all().exists(),
        )

    def test_course_retrieve(self):
        url = reverse("lms:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
