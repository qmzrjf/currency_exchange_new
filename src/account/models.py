from uuid import uuid4
from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from account.tasks import send_activation_code_async, send_sms_code_async
import random


def avatar_path(instace, filename: str):
    ext = filename.split('.')[-1]
    f = str(uuid4())
    filename = f'{f}.{ext}'
    return '/'.join(['avatar', str(instace.id), filename])


class User(AbstractUser):
    avatar = models.ImageField(upload_to=avatar_path, null=True, blank=True, default=None)
    phone = models.CharField(max_length=20)

class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=256)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class ActivationCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activation_codes')
    created = models.DateTimeField(auto_now_add=True)
    code = models.UUIDField(default=uuid4, editable=False, unique=True)
    is_activated = models.BooleanField(default=False)

    @property
    def is_expired(self):
        now = datetime.now()
        diff = now - self.created
        return diff.days > 7

    def send_activation_code(self):
        send_activation_code_async.delay(self.user.email, self.code)



def generate_sms_code():
    return random.randint(1000,32000)


class SmsCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activation_code_sms')
    created = models.DateTimeField(auto_now_add=True)
    code = models.PositiveSmallIntegerField(default=generate_sms_code)
    is_activated = models.BooleanField(default=False)

    @property
    def is_expired(self):
        now = datetime.now()
        diff = now - self.created
        return diff.days > 7

    def send_activation_sms_code(self):
        send_sms_code_async.delay(self.user.phone, self.code)
