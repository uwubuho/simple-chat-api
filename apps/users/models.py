"""
Models for users app
"""

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.db.models.base import Model
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver


class UserProfile(Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True, related_name='profile')
    nickname = models.CharField(max_length=150, null=False, default='Joe')
    description = models.CharField(max_length=255, blank=True, null=False)
    picture = models.ImageField(upload_to='profiles', default='default-user.png')

    @property
    def friends(self):
        return UserProfile.objects.filter(Q(buddies__fellow=self) | Q(fellows__buddy=self))


class Friendship(Model):
    fellow = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='fellows')
    buddy = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='buddies')

    def clean(self):
        condition = Q(fellow=self.buddy, buddy=self.fellow) | Q(fellow=self.fellow, buddy=self.buddy)
        exists = self.__class__.objects.filter(condition).exclude(id=self.id).exists()
        if exists:
            raise ValidationError(_("Friendship already exists beetween {} and {}".format(self.fellow, self.buddy)))
        if self.fellow == self.buddy:
            raise ValidationError(_("Can't declare friendship to yourself"))
        return super().clean()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.full_clean()
        return super().save(force_insert, force_update, using, update_fields)


@receiver(post_save, sender=get_user_model())
def create_user_profile(**kwargs):
    if kwargs['created']:
        instance = kwargs['instance']
        UserProfile.objects.create(user=instance, nickname=instance.username)
    kwargs['instance'].profile.save()
