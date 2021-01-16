"""
Views for users app
"""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from apps.users.serializers import FriendRequestSerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request, format=None):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def add_friend(request, username):
    to_user = get_user_model().objects.filter(username=username)
    if not to_user.exists():
        errors = { 'errors' : ['User with username {} was not found'.format(username)] }
        return Response(errors, status.HTTP_400_BAD_REQUEST)
    data = {
        'from_user': request.user, 'to_user' : to_user[0]
    }
    serializer = FriendRequestSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
