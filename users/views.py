from rest_framework import generics, permissions
from users.models import Payment
from users.serializers import PaymentSerializer, MyTokenObtainPairSerializer
from django_filters import rest_framework as filters
from users.serializers import PaymentSerializer, UserSerializer, UserUpdateSerializer
from users.models import User
from rest_framework_simplejwt.views import TokenObtainPairView


class PaymentFilter(filters.FilterSet):
    class Meta:
        model = Payment
        fields = {
            "payment_date": ["exact", "gte", "lte"],
            "paid_course": ["exact"],
            "paid_lesson": ["exact"],
            "payment_method": ["exact"],
        }


class PaymentList(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PaymentFilter


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]  # Доступно для всех


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Позволяет пользователям видеть и редактировать только свои данные
        return self.request.user


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
