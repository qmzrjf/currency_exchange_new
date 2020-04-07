from django.http import HttpResponse, JsonResponse
import json
from rest_framework import generics

from currency.api.serializers import RateSerializer
from currency.models import Rate
from django_filters import rest_framework as filters


class RateFilter(filters.FilterSet):
    created = filters.NumberFilter(field_name="created", lookup_expr='exact')
    created__lt = filters.NumberFilter(field_name="created", lookup_expr='lt')
    created__gt = filters.NumberFilter(field_name="created", lookup_expr='gt')
    created__lte = filters.NumberFilter(field_name="created", lookup_expr='lte')
    created__gte = filters.NumberFilter(field_name="created", lookup_expr='gte')
    currency = filters.NumberFilter(field_name="currency", lookup_expr='exact')
    source = filters.NumberFilter(field_name="source", lookup_expr='exact')

    class Meta:
        model = Rate
        fields = ['created', 'currency', 'source']


class RatesView(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = RateFilter


class RateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
