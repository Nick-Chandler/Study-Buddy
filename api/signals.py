from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import UserFile

@receiver(post_delete, sender=UserFile)
def delete_userfile_file(sender, instance, **kwargs):
  if instance.file:
    instance.file.delete(save=False)