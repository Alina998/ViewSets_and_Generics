from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name="Почта")
    phone_number = models.CharField(
        max_length=35, blank=True, null=True, verbose_name="Номер телефона"
    )
    user_country = models.CharField(
        max_length=56, blank=True, null=True, verbose_name="Страна"
    )
    user_photo = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Фото",
        help_text="Загрузите фото",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
