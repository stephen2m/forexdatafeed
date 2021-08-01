"""
WSGI config for forexDataFeed project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from configurations.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.development')
os.environ.setdefault('DJANGO_CONFIGURATION', 'development')

application = get_wsgi_application()
