"""
Admin registries for users app
"""

from django.contrib import admin
from apps.users.models import UserProfile

admin.site.register(UserProfile)
