from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="courses/preview",
        blank=True,
        null=True,
        verbose_name="Превью курса",
        help_text="Загрузите изображение",
    )
    description = models.CharField(max_length=500, verbose_name="Описание курса")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название урока")
    description = models.CharField(max_length=500, verbose_name="Описание урока")
    preview = models.ImageField(
        upload_to="courses/preview",
        blank=True,
        null=True,
        verbose_name="Превью урока",
        help_text="Загрузите изображение",
    )
    video_link = models.URLField(max_length=200, verbose_name="Ссылка на видео")
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Выберите курс",
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
