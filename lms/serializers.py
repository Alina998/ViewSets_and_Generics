from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from lms.validators import VideoLinkValidator
from users.models import Subscription
from lms.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    """Сериализатор для уроков"""

    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [
            VideoLinkValidator(field="video_link")
        ]  # Валидация ссылки на видео


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курсов"""

    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField()  # Поле для проверки подписки

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, obj):
        return obj.lesson_set.count()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user  # Получаем текущего пользователя
        if user.is_authenticated:
            return Subscription.objects.filter(
                user=user, course=obj
            ).exists()  # Проверяем наличие подписки
        return False
