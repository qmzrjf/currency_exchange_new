from django.http import HttpResponse, JsonResponse
import json
from rest_framework import generics

from account.api.serializers import ContactSerializer
from account.api.pagination import ContactResultsSetPagination
from account.models import Contact
from django_filters import rest_framework as filters
from account.tasks import send_emial_aync

from django.conf import settings


class ContactFilter(filters.FilterSet):
    subject = filters.NumberFilter(field_name="subject", lookup_expr='exact')
    email = filters.NumberFilter(field_name="email", lookup_expr='exact')

    class Meta:
        model = Contact
        fields = ['subject', 'email']


class ContactsView(generics.ListCreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ContactFilter
    pagination_class = ContactResultsSetPagination

    def get_queryset(self):
        super().get_queryset()
        self.queryset = Contact.objects.filter(email=self.request.user.email)
        return self.queryset


class ContactView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    pagination_class = ContactResultsSetPagination

    def get_queryset(self):
        super().get_queryset()
        self.queryset = Contact.objects.filter(email=self.request.user.email)
        return self.queryset
