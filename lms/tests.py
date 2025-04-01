from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from lms.models import Course, Lesson
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
import unittest


User = get_user_model()


class CourseAPITestCase(APITestCase):
    def setUp(self):
        # Создание тестового пользователя
        self.user = User.objects.create_user(username='User_1', email='user_1@example.com', password='password')
        self.client.login(email='user_1@example.com', password='password')

        # Создание тестового курса
        self.course = Course.objects.create(name='Test Course', description='Test Description')

        # URL для тестов
        self.course_url = reverse('course-detail', args=[self.course.id])
        self.lesson_url = reverse('lesson-list')

    def test_create_course(self):
        # Тестирование создания курса
        data = {'name': 'New Course', 'description': 'New Description'}
        response = self.client.post(reverse('course-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)  # Проверяем, что курс создан

    def test_get_course(self):
        # Тестирование получения курса
        response = self.client.get(self.course_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Course')

    def test_update_course(self):
        # Тестирование обновления курса
        data = {'name': 'Updated Course', 'description': 'Updated Description'}
        response = self.client.put(self.course_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.name, 'Updated Course')

    def test_delete_course(self):
        # Тестирование удаления курса
        response = self.client.delete(self.course_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)  # Проверяем, что курс удалён

class LessonAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        self.course = Course.objects.create(name='Test Course', description='Test Description')
        self.lesson = Lesson.objects.create(name='Test Lesson', description='Test Lesson Description', course=self.course)

        self.lesson_url = reverse('lesson-detail', args=[self.lesson.id])

    def test_create_lesson(self):
        # Тестирование создания урока
        data = {'name': 'New Lesson', 'description': 'New Lesson Description', 'course': self.course.id}
        response = self.client.post(reverse('lesson-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)  # Проверяем, что урок создан

    def test_get_lesson(self):
        # Тестирование получения урока
        response = self.client.get(self.lesson_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Lesson')

    def test_update_lesson(self):
        # Тестирование обновления урока
        data = {'name': 'Updated Lesson', 'description': 'Updated Lesson Description', 'course': self.course.id}
        response = self.client.put(self.lesson_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, 'Updated Lesson')

    def test_delete_lesson(self):
        # Тестирование удаления урока
        response = self.client.delete(self.lesson_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)  # Проверяем, что урок удалён

class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        self.course = Course.objects.create(name='Test Course', description='Test Description')

    def test_subscribe_to_course(self):
        # Тестирование подписки на курс
        response = self.client.post(reverse('subscribe', args=[self.course.id]))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_check_subscription_status(self):
        # Сначала подписываем пользователя на курс
        self.client.post(reverse('subscribe', args=[self.course.id]))

        # Теперь проверяем статус подписки
        response = self.client.get(reverse('subscribe', args=[self.course.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['subscribed'])  # Проверяем, что пользователь подписан на курс

if __name__ == '__main__':
    unittest.main()
