"""
Views Tests for users app
"""

from django.contrib.auth import get_user_model
from django.test.testcases import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


class ViewTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.add_friend_url = reverse('add_friend', args=('idontexists',))

    def test_register_view_does_not_allow_get(self):
        """
        Register View does not allow get
        """
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 405)

    def test_add_friend_user_not_found(self):
        """
        Add Friend View gives error if user not found
        """
        User = get_user_model()
        user = User.objects.create_user(username='jack', email='j@j.com', password='jacky')
        token = RefreshToken.for_user(user).access_token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token))
        response = self.client.get(self.add_friend_url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), { 'errors' : ['User with username idontexists was not found'] })
    
    def test_accept_friend_request(self):
        """
        User can accept friend requests
        """
        User = get_user_model()
        jack = User.objects.create_user(username='jack', password='jack')
        cooper = User.objects.create_user(username='cooper', password='cooper')
        token_jack = RefreshToken.for_user(jack).access_token
        token_cooper = RefreshToken.for_user(cooper).access_token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token_cooper))
        friend_request = self.client.get(reverse('add_friend', args=('jack',))).json()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token_jack))
        response = self.client.get(reverse('accept_friend_request', args=(friend_request['id'],)))
        self.assertEqual(response.status_code, 201)


    def test_reject_friend_request(self):
        """
        User can reject friend requests
        """
        User = get_user_model()
        jack = User.objects.create_user(username='jack', password='jack')
        cooper = User.objects.create_user(username='cooper', password='cooper')
        token_jack = RefreshToken.for_user(jack).access_token
        token_cooper = RefreshToken.for_user(cooper).access_token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token_cooper))
        friend_request = self.client.get(reverse('add_friend', args=('jack',))).json()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token_jack))
        response = self.client.get(reverse('reject_friend_request', args=(friend_request['id'],)))
        self.assertEqual(response.status_code, 200)