"""
Consumers Tests for chat app
"""

from django.test.testcases import SimpleTestCase
from channels.testing import WebsocketCommunicator
from config.asgi import application


class ConsumerTests(SimpleTestCase):

    async def test_echo_consumer(self):
        """
        Echo Consumer sends back the message
        """
        communicator = WebsocketCommunicator(application, "/ws/echo/")
        connected = await communicator.connect()
        self.assertTrue(connected)
        text_data = "test1234"
        await communicator.send_to(text_data=text_data)
        response = await communicator.receive_from()
        self.assertEqual(response, text_data)
        await communicator.disconnect()
