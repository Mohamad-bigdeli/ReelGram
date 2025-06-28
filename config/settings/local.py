from .base import *
from decouple import config


if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
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