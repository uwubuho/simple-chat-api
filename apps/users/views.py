"""
Views for users app
"""

from apps.users import serializers
from apps.users.models import FriendRequest
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from apps.users.serializers import FriendRequestSerializer, PublicUserProfileSerializer, UserSerializer


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
        return Response(errors, status.HTTP_404_NOT_FOUND)
    data = {
        'from_user': request.user, 'to_user' : to_user[0]
    }
    serializer = FriendRequestSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def accept_friend_request(request, request_id):
    friend_request = FriendRequest.objects.filter(pk=request_id)
    if friend_request.exists():
        profile_user = friend_request[0].to_user
        serializer = PublicUserProfileSerializer(profile_user)
        friend_request[0].accept()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        errors = { 'errors' : ['Friend request with id {} does not exists'.format(request_id)]}
        return Response(errors, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def reject_friend_request(request, request_id):
    friend_request = FriendRequest.objects.filter(pk=request_id)
    if friend_request.exists():
        profile_user = friend_request[0].to_user
        serializer = PublicUserProfileSerializer(profile_user)
        friend_request[0].reject()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        errors = { 'errors' : ['Friend request with id {} does not exists'.format(request_id)]}
        return Response(errors, status=status.HTTP_404_NOT_FOUND)