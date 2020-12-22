"""
URLs for chat app
"""

from django.urls import path
from apps.chat import views

urlpatterns = [
    path('ping/', views.PingPongView.as_view(), name='ping'),
    path('auth/ping/', views.AuthPingPongView.as_view(), name='auth_ping'),
]
