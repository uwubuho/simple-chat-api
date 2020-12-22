"""
Models Tests for users app
"""

from django.core.exceptions import ValidationError
from django.test.testcases import TestCase
from django.contrib.auth import get_user_model
from django.db import transaction
from apps.users.models import Friendship, UserProfile


class ModelsTests(TestCase):

    def test_create_user_profile(self):
        """
        Creates profile when user is created
        """
        User = get_user_model() # pylint: disable=invalid-name
        user = User.objects.create_user(username='someuser', email='example@user.com', password='1234')
        profile = UserProfile.objects.get(pk=user)
        self.assertEqual(profile, user.profile)
        self.assertEqual(profile.user.username, 'someuser')
        self.assertEqual(profile.user.email, 'example@user.com')
        self.assertEqual(profile.nickname, user.username)

    def test_cant_create_duplicated_friendships(self):
        """
        Does not allow duplicated friendships
        """
        User = get_user_model() # pylint: disable=invalid-name
        fellow = User.objects.create_user(username='fellow', email='fellow@user.com', password='1234').profile
        buddy = User.objects.create_user(username='buddy', email='buddy@user.com', password='1234').profile
        Friendship.objects.create(fellow=fellow, buddy=buddy)
        with transaction.atomic():
            self.assertRaises(ValidationError, Friendship.objects.create, fellow=fellow, buddy=buddy)
        with transaction.atomic():
            self.assertRaises(ValidationError, Friendship.objects.create, fellow=buddy, buddy=fellow)

    def test_friends_property_works(self):
        """
        Friends property works
        """
        User = get_user_model() # pylint: disable=invalid-name
        user = User.objects.create_user(username='joe', email='joe@user.com', password='1234').profile
        friend1 = User.objects.create_user(username='friendjoe1', email='joe1@user.com', password='1234').profile
        friend2 = User.objects.create_user(username='friendjoe2', email='joe2@user.com', password='1234').profile
        lonelyone = User.objects.create_user(username='lonelyone', email='lonelyone@user.com', password='1234').profile
        Friendship.objects.create(fellow=user, buddy=friend1)
        Friendship.objects.create(fellow=friend2, buddy=user)
        Friendship.objects.create(fellow=friend1, buddy=friend2)
        self.assertTrue(user.friends.filter(pk=friend1).exists())
        self.assertTrue(user.friends.filter(pk=friend2).exists())
        self.assertFalse(user.friends.filter(pk=lonelyone).exists())
        self.assertTrue(friend1.friends.filter(pk=friend2).exists())
        self.assertTrue(friend1.friends.filter(pk=user).exists())
