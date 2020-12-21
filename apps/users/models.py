"""
Models for users app
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.base import Model
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver


class UserProfile(Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True, related_name='profile')
    nickname = models.CharField(max_length=150, null=False, default="Joe")
    description = models.CharField(max_length=255, blank=True, null=False)
    picture = models.ImageField(upload_to='profiles', default='default-user.png')


@receiver(post_save, sender=get_user_model())
def create_user_profile(**kwargs):
    if kwargs['created']:
        instance = kwargs['instance']
        UserProfile.objects.create(user=instance, nickname=instance.username)
    kwargs['instance'].profile.save()
