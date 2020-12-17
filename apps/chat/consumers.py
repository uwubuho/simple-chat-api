"""
Channels Consumers for chat app
"""

from channels.generic.websocket import WebsocketConsumer


class EchoConsumer(WebsocketConsumer):
    """
    Sends back the message
    """

    def connect(self):
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        self.send(text_data=text_data, bytes_data=bytes_data)
