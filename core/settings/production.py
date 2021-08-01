from .base import BaseConfiguration


class Production(BaseConfiguration):
    # Apps
    INSTALLED_APPS = BaseConfiguration.INSTALLED_APPS
    INSTALLED_APPS += ['gunicorn']
