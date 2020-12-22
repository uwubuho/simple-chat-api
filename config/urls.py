"""
Project URL Configuration
"""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.chat.urls')),
    path('users/', include('apps.users.urls')),
]
