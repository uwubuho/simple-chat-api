"""
Models Tests for users app
"""

from django.test.testcases import TestCase
from django.contrib.auth import get_user_model
from apps.users.models import UserProfile


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
