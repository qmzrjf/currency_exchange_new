from django.db.models.signals import pre_save
from django.dispatch import receiver

from account.models import User


@receiver(pre_save, sender=User)
def pre_save_user_avatar(sender, instance, **kwargs):
    # User.objects.filter().last().delete()
    pass