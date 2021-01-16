"""
URLs for users app
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.users.views import add_friend, register

urlpatterns = [
    path('register/', register, name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='access_token'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),

    path('add_friend/<username>/', add_friend, name='add_friend')
]
