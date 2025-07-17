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
    INSTALLED_APPS += [
        "debug_toolbar",
        "drf_spectacular",
        ]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

INTERNAL_IPS = [
    "127.0.0.1",
]

AUTH_USER_MODEL = "users.User"

SESSION_COOKIE_SECURE = False 
CSRF_COOKIE_SECURE = False   
SESSION_COOKIE_HTTPONLY = True  
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax' 
CSRF_COOKIE_SAMESITE = 'Lax'       