"""
Views for chat app
"""

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class PingPongView(APIView):
    """
    Pongs to Pings
    """

    permission_classes = [AllowAny]
    def get(self, request):
        return Response({'result': 'Pong!'}, status=status.HTTP_200_OK)


class AuthPingPongView(APIView):
    """
    Pongs to Pings only if user is authenticated
    """

    def get(self, request):
        return Response({'result': 'Secure pong!'}, status=status.HTTP_200_OK)
