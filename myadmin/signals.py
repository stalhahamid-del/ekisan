# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import Users
from django.core.cache import cache

@receiver(post_save, sender=Users)
def notify_new_farmer(sender, instance, created, **kwargs):
    if created and hasattr(instance, 'role') and instance.role == 'Farmer':  # Assuming 'role' is an attribute of User model
        message = f"New farmer added: {instance.name}"
        print(f"Signal triggered: {message}")
    elif created and hasattr(instance, 'role') and instance.role == 'Dealer':  # Assuming 'role' is an attribute of User model
        message = f"New Dealer added: {instance.name}"
        print(f"Signal triggered: {message}")    