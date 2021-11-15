from .models import CustomUser, UserProfile
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver


@receiver(post_save, sender=CustomUser)
def update_profile_signal(sender, instance, created, **kwargs):
    print('post_save')
    if created:
        UserProfile.objects.create(user=instance)


@receiver(pre_save, sender=CustomUser)
def update_profile_signal_pre_save(sender, instance, **kwargs):
    print("pre_save")
