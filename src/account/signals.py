from django.db.models.signals import pre_save
from django.dispatch import receiver

from account.models import User
import os

import shutil
from django.conf import settings


@receiver(pre_save, sender=User)
def pre_save_user_avatar(sender, instance, **kwargs):

    try:
        if instance.avatar:
            shutil.rmtree(os.path.join(settings.MEDIA_ROOT, 'avatar', str(instance.id)))
    except:
        pass
