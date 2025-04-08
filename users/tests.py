from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User, Subscription, Payment
from lms.models import Course, Lesson


class UserTestCase(APITestCase):
    """Тестирование модели пользователя"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword", username="test_user"
        )
        self.course = Course.objects.create(name="Test Course")
        self.lesson = Lesson.objects.create(name="Test Lesson", course=self.course)

    def test_create_user(self):
        """Тест для создания пользователя"""
        url = reverse("users:user-register")
        data = {
            "email": "newuser@example.com",
            "password": "newpassword",
            "username": "newuser",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)  # Один существующий + один новый

    def test_get_user(self):
        """Тест для просмотра данных пользователя"""
        self.client.force_authenticate(self.user)
        url = reverse("users:user-detail", args=[self.user.id])
        response = self.client.get(url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get("email"), self.user.email)


class SubscriptionTestCase(APITestCase):
    """Тест модели подписки"""

    def setUp(self) -> None:
        """Создаем тестового пользователя"""
        self.user = User.objects.create(
            email="testuser@example.com", password="testpassword", username="test_user"
        )
        self.user.set_password("test_pass_2")
        self.user.save()
        self.client.force_authenticate(user=self.user)

        """Создаем тестовоый курс"""
        self.course = Course.objects.create(
            name="test course sub", description="test desc sub"
        )

        """Создаем подписку"""
        self.subscription = Subscription.objects.create(
            user=self.user, course=self.course
        )

    def test_create_subscription(self):
        """Тестирование создания подписки"""

        course = Course.objects.create(
            name="test course sub 2", description="test desc sub 2"
        )

        data = {
            "user": self.user.pk,
            "course": course.pk,
        }

        url = reverse("users:subscribe", args=(course.pk,))

        response = self.client.post(url, data=data)

        # subscription_url = reverse('subscribe')
        # print(subscription_url)
        # response = self.client.post(subscription_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.all().count(), 2)

    def test_list_subscription(self):
        """Тест для просмотра подписки"""
        subscription_url = reverse("users:subscriptions")
        print(subscription_url)
        response = self.client.get(subscription_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
