"""
Django settings for local environment
"""

import os
from .base import BASE_DIR

SECRET_KEY = '=27m8#u7o2bq%k-hg(_^n!i6av1jm(^z_)boh7*=%za9e63_-2'
DEBUG = True
ALLOWED_HOSTS = []

CHANNEL_LAYERS = {
   "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": ['redis://localhost:6379'],
        }
    },
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME' : 'chat',
        'USER' : 'chat',
        'PASSWORD' : 'chat',
        'HOST' : 'localhost',
        'PORT' : '5432'
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
