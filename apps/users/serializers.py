"""
REST Serializers for users app
"""

from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password')
        extra_kwargs = { 'password': { 'write_only': True }, 'email' : { 'required' : True } }

    def create(self, validated_data):
        User = get_user_model()
        user = User.objects.create_user(**validated_data)
        user.save()
        return user
