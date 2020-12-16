"""
Views for chat app
"""

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class PingPongView(APIView):
    """
    Pongs to Pings
    """
    def get(self, request):
        return Response({ 'result' : 'Pong!' }, status=status.HTTP_200_OK)
