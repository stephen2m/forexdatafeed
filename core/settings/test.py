import logging

from .base import BaseConfiguration


class Test(BaseConfiguration):
    # Debug
    DEBUG = True

    CELERY_ALWAYS_EAGER = True

    # Testing
    INSTALLED_APPS = BaseConfiguration.INSTALLED_APPS

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        },
    }

    # disable logging middleware
    logging.getLogger('api_requests').disabled = True
