from rest_framework import generics, permissions
from users.models import Payment, Subscription, User
from django_filters import rest_framework as filters
from users.serializers import PaymentSerializer, UserSerializer, UserUpdateSerializer, SubscriptionSerializer, MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from lms.paginators import CustomPageNumberPagination
import stripe
from django.conf import settings
from django.views import View
from django.http import JsonResponse
from django.shortcuts import render

stripe.api_key = settings.STRIPE_TEST_SECRET_KEY


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
    pagination_class = CustomPageNumberPagination


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


class SubscriptionCreateView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Только авторизованные пользователи могут подписываться

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)  # Устанавливаем текущего пользователя как создателя подписки


class SubscriptionListView(generics.ListAPIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Только авторизованные пользователи могут просматривать свои подписки
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        # Возвращаем подписки только для текущего пользователя
        user = self.request.user
        return Subscription.objects.filter(user=user)


class SubscriptionDeleteView(generics.DestroyAPIView):
    queryset = Subscription.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Получаем объект подписки по текущему пользователю и курсу
        return Subscription.objects.get(user=self.request.user, course=self.kwargs['course_id'])


stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

class CreateProductView(View):
    def post(self, request):
        try:
            product = stripe.Product.create(
                name=request.POST.get('name'),
                description=request.POST.get('description'),
            )
            return JsonResponse({'product_id': product.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})

class CreatePriceView(View):
    def post(self, request):
        try:
            price = stripe.Price.create(
                unit_amount=int(request.POST.get('amount')),  # сумма
                currency='usd',
                product=request.POST.get('product_id'),
            )
            return JsonResponse({'price_id': price.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})

class CreateCheckoutSessionView(View):
    def post(self, request):
        try:
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price': request.POST.get('price_id'),
                    'quantity': 1,
                }],
                mode='payment',
                success_url='https://your-domain.com/success',
                cancel_url='https://your-domain.com/cancel',
            )
            return JsonResponse({'session_id': session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)})
