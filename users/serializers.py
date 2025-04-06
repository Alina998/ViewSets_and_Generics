from rest_framework import serializers
from lms.models import Course, Lesson
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users.models import User, Payment, Subscription


class PaymentSerializer(serializers.ModelSerializer):
    """Сериализатор для платежей"""

    user_email = serializers.EmailField(
        source="user.email", read_only=True
    )  # Добавляем поле email пользователя
    paid_course_name = serializers.CharField(
        source="paid_course.name", read_only=True
    )  # Название оплаченного курса
    paid_lesson_name = serializers.CharField(
        source="paid_lesson.name", read_only=True
    )  # Название оплаченного урока

    class Meta:
        model = Payment
        fields = [
            "id",
            "user_email",
            "payment_date",
            "paid_course_name",
            "paid_lesson_name",
            "amount",
            "payment_method",
        ]


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Сериализатор для получения токена"""

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавление пользовательских полей в токен
        token["username"] = user.username
        token["email"] = user.email

        return token


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя"""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone_number",
            "user_country",
            "user_photo",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор для обновления данных пользователя"""

    class Meta:
        model = User
        fields = ["phone_number", "user_country", "user_photo"]


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки"""

    class Meta:
        model = Subscription
        fields = ["user", "course"]
        read_only_fields = ["user"]  # Пользователь будет определяться автоматически
