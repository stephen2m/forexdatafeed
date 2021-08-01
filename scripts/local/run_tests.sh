#!/bin/sh

export DJANGO_SETTINGS_MODULE="core.settings.test"
export DJANGO_CONFIGURATION="Test"
python manage.py test
