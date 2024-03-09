from django.conf import settings
from django.db.models.signals import post_delete
from django.dispatch import receiver
from buy_car.models import Captcha
import os

@receiver(post_delete, sender=Captcha)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
