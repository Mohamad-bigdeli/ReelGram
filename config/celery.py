import os
from decouple import config
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', config("DJANGO_SETTINGS_MODULE"))

app = Celery('config', broker=settings.CELERY_BROKER_URL)
app.config_from_object('django.conf:settings', namespace='CELERY')
app.config_defaults = {"broker_connection_retry_on_startup": True}
app.autodiscover_tasks([])