from uuid import uuid4

from django.db import models
from django.contrib.auth.models import AbstractUser


def avatar_path(instace, filename:str):
    ext = filename.split('.')[-1]
    f = str(uuid4())
    filename = f'{f}.{ext}'
    return '/'.join(['avatar', str(instace.id), filename])

class User(AbstractUser):
    avatar = models.ImageField(upload_to=avatar_path, null=True, blank = True, default=None)


class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=256)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
