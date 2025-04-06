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
        url = reverse("user-register")
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
        url = reverse("user-detail", args=[self.user.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)


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

        data = {
            "user": self.user.pk,
            "course": self.course.pk,
        }

        response = self.client.post(
            f"subscribe/{self.subscription.course_id}/", data=data
        )
        print(response.json())

        # subscription_url = reverse('subscribe')
        # print(subscription_url)
        # response = self.client.post(subscription_url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscription.objects.all().count(), 2)

    def test_list_subscription(self):
        """Тест для просмотра подписки"""
        subscription_url = reverse("subscriptions")
        print(subscription_url)
        response = self.client.get(subscription_url)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)


class PaymentTests(APITestCase):
    """Тест модели платежей"""

    def setUp(self):
        self.user = User.objects.create_user(
            email="testuser@example.com", password="testpassword", username="test_user"
        )
        self.course = Course.objects.create(name="Test Course")
        self.lesson = Lesson.objects.create(name="Test Lesson", course=self.course)

    def test_create_payment(self):
        """Тест для создания платежа"""
        url = reverse("payment-list")
        data = {
            "user": self.user.id,
            "paid_course": self.course.id,
            "amount": 100.00,
            "payment_method": "cash",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_payment(self):
        """Тест для просмотра данных платежа"""
        payment = Payment.objects.create(
            user=self.user,
            paid_course=self.course,
            amount=100.00,
            payment_method="cash",
        )

        url = reverse("create-checkout-session/", args=[payment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
