"""
Views Tests for chat app
"""

import json
from django.test.testcases import SimpleTestCase
from django.urls import reverse
from rest_framework.test import APIClient


class ViewTests(SimpleTestCase):

    def setUp(self):
        self.client = APIClient()
        self.ping_url = reverse('ping')

    def test_ping_view_post(self):
        """
        Ping View does not allow POST requests
        """
        response = self.client.post(self.ping_url, {'anything': 'another thing'})
        self.assertEqual(response.status_code, 405)

    def test_ping_view_get(self):
        """
        Ping View responds 'Pong!'
        """
        response = self.client.get(self.ping_url)
        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(json.loads(response.content), {'result': 'Pong!'})
