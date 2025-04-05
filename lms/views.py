from rest_framework.viewsets import ModelViewSet
from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from lms.paginators import CustomPageNumberPagination


class CourseViewSet(ModelViewSet):
    '''Вьюсет для курса'''
    serializer_class = CourseSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        if self.request.user.groups.filter(name="Moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(user=self.request.user)

    def get_serializer_context(self):  # Добавляем метод для передачи контекста
        context = super().get_serializer_context()
        context['request'] = self.request  # Передаем текущий запрос
        return context

    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def perform_create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonList(generics.ListCreateAPIView):
    '''Представление для списка уроков'''
    serializer_class = LessonSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        if self.request.user.groups.filter(name="Moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(user=self.request.user)

    @api_view(["POST"])
    @permission_classes([IsAuthenticated])
    def perform_create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonRetrieve(generics.RetrieveAPIView):
    '''Представление для просмотра урока'''
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonCreate(generics.CreateAPIView):
    '''Представление для создания урока'''
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonUpdate(generics.UpdateAPIView):
    '''Представление для обновления урока'''
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonDestroy(generics.DestroyAPIView):
    '''Представление для удаления урока'''
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
