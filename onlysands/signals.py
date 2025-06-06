from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    
@receiver(pre_save, sender=User)
def lowercase_email(sender, instance, **kwargs):
    if instance.email:
        instance.email = instance.email.strip().lower()
