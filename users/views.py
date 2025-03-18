from rest_framework import generics
from users.models import Payment
from users.serializers import PaymentSerializer
from django_filters import rest_framework as filters
from users.serializers import PaymentSerializer

class PaymentFilter(filters.FilterSet):
    class Meta:
        model = Payment
        fields = {
            'payment_date': ['exact', 'gte', 'lte'],
            'paid_course': ['exact'],
            'paid_lesson': ['exact'],
            'payment_method': ['exact'],
        }

class PaymentList(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = PaymentFilter

