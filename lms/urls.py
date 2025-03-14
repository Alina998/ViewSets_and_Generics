from django.urls import path, include
from rest_framework.routers import SimpleRouter
from lms.apps import LmsConfig
from lms.views import (
    CourseViewSet,
    LessonList,
    LessonRetrieve,
    LessonCreate,
    LessonUpdate,
    LessonDestroy,
)


app_name = LmsConfig.name

router = SimpleRouter()
router.register(r"courses", CourseViewSet, basename="course")

urlpatterns = [
    path("", include(router.urls)),
    path("lessons/", LessonList.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", LessonRetrieve.as_view(), name="lesson-detail"),
    path("lessons/create/", LessonCreate.as_view(), name="lesson-create"),
    path("lessons/update/<int:pk>/", LessonUpdate.as_view(), name="lesson-update"),
    path("lessons/delete/<int:pk>/", LessonDestroy.as_view(), name="lesson-delete"),
]
