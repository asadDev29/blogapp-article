from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Writer

@receiver(post_save, sender=User)
def create_writer(sender, instance, created, **kwargs):
    if created:
        Writer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_writer(sender, instance, **kwargs):
    instance.writer.save()
