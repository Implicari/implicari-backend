# flake8: noqa: F405

from decouple import Csv

from .base import *


ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
DEBUG = True
SECRET_KEY = 'i_am_a_super_secret_key'

INSTALLED_APPS += [
    'django_extensions',
]

if config('DEBUG_TOOLBAR', False):
    INSTALLED_APPS += [
        'debug_toolbar',
    ]

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

else:
    pass
