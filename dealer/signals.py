from django.db import models
from farmer.models import Message
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import messages
from dealer.models import Bit
from django.utils import timezone

@receiver(post_save, sender=Bit)
def send_acceptance_notification(sender, instance, **kwargs):
    if instance.status:
        message = f'Your bit for {instance.product} is accepted by the {instance.farmer} .'
        Message.objects.create(user=instance.bitter, product=instance.product, notification=message)

