from .base import *
from decouple import config


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

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

INTERNAL_IPS = [
    "127.0.0.1",
]