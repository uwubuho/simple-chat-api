"""
URLs for users app
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from apps.users.views import register

urlpatterns = [
    path('register/', register, name='register'),
    path('auth/token/', TokenObtainPairView.as_view(), name='access_token'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
]
