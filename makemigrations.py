#!/usr/bin/env python
import os
import sys

from django.conf import settings
from django.core.management import call_command
import django

DEFAULT_SETTINGS = dict(
    INSTALLED_APPS=(
        'django.contrib.contenttypes',
        'django_learnit',
    ),
)


def makemigrations():
    if not settings.configured:
        settings.configure(**DEFAULT_SETTINGS)

    if hasattr(django, 'setup'):
        django.setup()

    parent = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, parent)

    call_command('makemigrations', 'django_learnit')


if __name__ == '__main__':
    makemigrations()
