from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from lms.models import Course, Lesson
from django.contrib.auth.models import Group
# from users.models import User
from django.contrib.auth import get_user_model


User = get_user_model()


class LessonTests(APITestCase):

    def setUp(self):
        # Создаем пользователей и группы
        self.moderator_group = Group.objects.create(name='Moderators')
        self.user = User.objects.create_user(username='User_1', email='user_1@example.com', password='password')
        self.moderator = User.objects.create_user(username='moderator', password='password')
        self.moderator.groups.add(self.moderator_group)

        # Создаем курс и уроки
        self.course = Course.objects.create(name='Test Course', description='Test Description')
        self.lesson = Lesson.objects.create(name='Test Lesson', description='Test Lesson Description', video_link='http://testvideo.com', course=self.course)

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lms:lesson-list')
        data = {
            'name': 'New Lesson',
            'description': 'New Lesson Description',
            'video_link': 'http://youtube.com',
            'course': self.course.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lms:lesson-detail', args=[self.lesson.id])
        data = {
            'name': 'Updated Lesson',
            'description': 'Updated Lesson Description',
            'video_link': 'http://updatedvideo.com',
            'course': self.course.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, 'Updated Lesson')

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('lms:lesson-detail', args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_user_cannot_access_other_users_lessons(self):
        self.client.force_authenticate(user=self.user)
        other_course = Course.objects.create(name='Other Course', description='Other Description', user=self.user)
        other_lesson = Lesson.objects.create(name='Other Lesson', description='Other Lesson Description', video_link='http://testvideo.com', course=other_course)

        url = reverse('lms:lesson-detail', args=[other_lesson.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_moderator_can_access_all_lessons(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse('lms:lesson-detail', args=[self.lesson.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_cannot_create_lesson_without_authentication(self):
        url = reverse('lesson-list')
        data = {
            'name': 'Unauthorized Lesson',
            'description': 'Unauthorized Lesson Description',
            'video_link': 'http://unauthorizedvideo.com',
            'course': self.course.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_moderator_can_delete_any_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse('lms:lesson-detail', args=[self.lesson.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_user_can_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('subscribe', args=[self.course.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_moderator_can_subscribe_to_course(self):
        self.client.force_authenticate(user=self.moderator)
        url = reverse('subscribe', args=[self.course.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
