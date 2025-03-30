from django.urls import path
from users.views import (
    PaymentList,
    MyTokenObtainPairView,
    UserRegistrationView,
    UserDetailView,
    SubscriptionCreateView,
    SubscriptionDeleteView,
    SubscriptionListView
)

urlpatterns = [
    path("payments/", PaymentList.as_view(), name="payment-list"),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path('subscribe/', SubscriptionCreateView.as_view(), name='subscribe'),
    path('unsubscribe/<int:course_id>/', SubscriptionDeleteView.as_view(), name='unsubscribe'),
    path('subscriptions/', SubscriptionListView.as_view(), name='subscriptions'),
]
