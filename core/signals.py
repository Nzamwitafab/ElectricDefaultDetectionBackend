# core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from core.models import Profile

User = settings.AUTH_USER_MODEL  # Uses your custom User model

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a profile when a new user is created."""
    if created:
        Profile.objects.create(user=instance, role=instance.role)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Auto-save the profile when the user is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()