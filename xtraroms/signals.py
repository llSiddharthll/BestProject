from django.dispatch import receiver
from djoser.signals import user_activated
from .models import UserProfile

@receiver(user_activated)
def activate_profile(user, request, **kwargs):
    user.is_active = True
    UserProfile.objects.create(user = user)