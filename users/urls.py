from django.urls import path
from users.views import (
    PaymentList,
    MyTokenObtainPairView,
    UserRegistrationView,
    UserDetailView,
    SubscriptionCreateView,
    SubscriptionDeleteView,
    SubscriptionListView,
    CreateProductView,
    CreatePriceView,
    CreateCheckoutSessionView,
)

urlpatterns = [
    path("payments/", PaymentList.as_view(), name="payment-list"),
    path('create-product/', CreateProductView.as_view(), name='create_product'),
    path('create-price/', CreatePriceView.as_view(), name='create_price'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path("token/", MyTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("register/", UserRegistrationView.as_view(), name="user-register"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path('subscribe/<int:course_id>/', SubscriptionCreateView.as_view(), name='subscribe'),
    path('unsubscribe/<int:course_id>/', SubscriptionDeleteView.as_view(), name='unsubscribe'),
    path('subscriptions/', SubscriptionListView.as_view(), name='subscriptions'),
]
