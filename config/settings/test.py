from .base import *

DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': config("POSTGRES_DB"),
            'USER': config("POSTGRES_USER"),
            'PASSWORD': config("POSTGRES_PASSWORD"),
            'HOST': config("POSTGRES_HOST"),
            'PORT': config("POSTGRES_PORT"),
        }
    }

AUTH_USER_MODEL = "users.User"

RATELIMIT_ENABLE = False