"""
Models for users app
"""

from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q, constraints
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

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class FriendRequest(Model):
    from_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_requests')

    def save(self, *args, **kwargs):
        self.full_clean()
        requests = self.__class__.objects.filter(to_user=self.from_user, from_user=self.to_user).exclude(id=self.id)
        if requests.exists():
            return requests[0].accept()
        else:
            return super().save(*args, **kwargs)

    def clean(self):
        condition = Q(fellow=self.from_user, buddy=self.to_user) | Q(fellow=self.to_user, buddy=self.from_user)
        exists = Friendship.objects.filter(condition).exists()
        if exists:
            raise ValidationError(_("Friendship already exists beetween {} and {}".format(self.from_user, self.to_user)))
        if self.from_user == self.to_user:
            raise ValidationError(_("Can't declare friend request to yourself"))
        return super().clean()

    def accept(self):
        friendship = Friendship.objects.create(fellow=self.from_user, buddy=self.to_user)
        friendship.save()
        self.delete()
        return friendship

    def reject(self):
        self.delete()

    class Meta:
        constraints = [
            constraints.UniqueConstraint(fields=['from_user', 'to_user'], name='unique_request')
        ]


@receiver(post_save, sender=get_user_model())
def create_user_profile(**kwargs):
    if kwargs['created']:
        instance = kwargs['instance']
        UserProfile.objects.create(user=instance, nickname=instance.username)
    kwargs['instance'].profile.save()
