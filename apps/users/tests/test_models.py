"""
Models Tests for users app
"""

from django.core.exceptions import ValidationError
from django.test.testcases import TestCase
from django.contrib.auth import get_user_model
from apps.users.models import Friendship, FriendRequest, UserProfile


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
        self.assertRaises(ValidationError, Friendship.objects.create, fellow=fellow, buddy=buddy)
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

    def test_request_accept(self):
        """
        Friendship created and request deleted when accepting it
        """
        User = get_user_model() # pylint: disable=invalid-name
        ale = User.objects.create_user(username='ale', email='ale@user.com', password='1234').profile
        mey = User.objects.create_user(username='mey', email='mey@user.com', password='1234').profile
        request = FriendRequest.objects.create(from_user=ale, to_user=mey)
        self.assertTrue(FriendRequest.objects.filter(pk=request.id).exists())
        request.accept()
        self.assertTrue(ale.friends.filter(pk=mey).exists())
        self.assertTrue(mey.friends.filter(pk=ale).exists())
        self.assertFalse(FriendRequest.objects.filter(pk=request.id).exists())

    def test_request_reject(self):
        """
        Request deleted when rejecting it
        """
        User = get_user_model() # pylint: disable=invalid-name
        crunchy = User.objects.create_user(username='crunchy', email='crunchy@user.com', password='1234').profile
        buho = User.objects.create_user(username='buho', email='buho@user.com', password='1234').profile
        request = FriendRequest.objects.create(from_user=buho, to_user=crunchy)
        self.assertTrue(FriendRequest.objects.filter(pk=request.id).exists())
        request.reject()
        self.assertFalse(crunchy.friends.filter(pk=buho).exists())
        self.assertFalse(buho.friends.filter(pk=crunchy).exists())
        self.assertFalse(FriendRequest.objects.filter(pk=request.id).exists())

    def test_both_way_request(self):
        """
        Request auto accept when two requests exist both ways
        """
        User = get_user_model() # pylint: disable=invalid-name
        crunchy = User.objects.create_user(username='crunchy', email='crunchy@user.com', password='1234').profile
        buho = User.objects.create_user(username='buho', email='buho@user.com', password='1234').profile
        request_buho = FriendRequest.objects.create(from_user=buho, to_user=crunchy)
        request_crunchy = FriendRequest.objects.create(from_user=crunchy, to_user=buho)
        self.assertTrue(crunchy.friends.filter(pk=buho).exists())
        self.assertTrue(buho.friends.filter(pk=crunchy).exists())
        self.assertFalse(FriendRequest.objects.filter(pk=request_buho.id).exists())
        self.assertFalse(FriendRequest.objects.filter(pk=request_crunchy.id).exists())

    def test_cant_create_duplicated_request(self):
        """
        Can't create duplicated requests
        """
        User = get_user_model() # pylint: disable=invalid-name
        fellow = User.objects.create_user(username='fellow', email='fellow@user.com', password='1234').profile
        buddy = User.objects.create_user(username='buddy', email='buddy@user.com', password='1234').profile
        FriendRequest.objects.create(from_user=fellow, to_user=buddy)
        self.assertRaises(ValidationError, FriendRequest.objects.create, from_user=fellow, to_user=buddy)

    def test_cant_create_requests_when_already_friend(self):
        """
        Can't create requests when both users are already friends
        """
        User = get_user_model() # pylint: disable=invalid-name
        crunchy = User.objects.create_user(username='crunchy', email='crunchy@user.com', password='1234').profile
        buho = User.objects.create_user(username='buho', email='buho@user.com', password='1234').profile
        self.assertFalse(crunchy.friends.filter(pk=buho).exists())
        request = FriendRequest.objects.create(from_user=buho, to_user=crunchy)
        request.accept()
        self.assertTrue(crunchy.friends.filter(pk=buho).exists())
        self.assertRaises(ValidationError, FriendRequest.objects.create, from_user=buho, to_user=crunchy)
        self.assertRaises(ValidationError, FriendRequest.objects.create, from_user=crunchy, to_user=buho)
