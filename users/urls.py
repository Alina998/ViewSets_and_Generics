from django.urls import path
from users.views import PaymentList

urlpatterns = [
    path('payments/', PaymentList.as_view(), name='payment-list'),
]
