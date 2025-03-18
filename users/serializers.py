from rest_framework import serializers
from users.models import Payment
from lms.models import Course, Lesson  # Импортируем Course и Lesson для сериализации

class PaymentSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)  # Добавляем поле email пользователя
    paid_course_name = serializers.CharField(source='paid_course.name', read_only=True)  # Название оплаченного курса
    paid_lesson_name = serializers.CharField(source='paid_lesson.name', read_only=True)  # Название оплаченного урока

    class Meta:
        model = Payment
        fields = ['id', 'user_email', 'payment_date', 'paid_course_name', 'paid_lesson_name', 'amount', 'payment_method']
