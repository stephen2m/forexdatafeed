import os

import configurations
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Development')

# https://django-configurations.readthedocs.io/en/stable/cookbook/#id4
configurations.setup()

app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
