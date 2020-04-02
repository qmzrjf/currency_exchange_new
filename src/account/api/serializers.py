from account.models import Contact
from rest_framework import serializers
from account.tasks import send_emial_aync
from django.conf import settings


class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = (
            'id',
            'email',
            'subject',
            'text',
        )

        # def create(self, validated_data):
        #     email = (self.validated_data['email'],)
        #     message = self.validated_data['text']
        #     subject = self.validated_data['subject']
        #     email_from = settings.EMAIL_HOST_USER
        #     send_emial_aync.delay(subject, message, email_from, email)
        #
        #     return Contact(**validated_data)
