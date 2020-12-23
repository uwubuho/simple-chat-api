"""
Views Tests for users app
"""

import json
from django.test.testcases import SimpleTestCase
from django.urls import reverse
from rest_framework.test import APIClient


class ViewTests(SimpleTestCase):

    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')

    def test_register_view_does_not_allow_get(self):
        """
        Register View does not allow get
        """
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 405)
