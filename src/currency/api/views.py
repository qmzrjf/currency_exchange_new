from django.http import HttpResponse, JsonResponse
import json
from rest_framework import generics

from currency.api.serializers import RateSerializer
from currency.models import Rate


class RatesView(generics.ListCreateAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer


class RateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer