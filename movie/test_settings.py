from .settings import *  # NOQA

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}

SCHEDULER_AUTOSTART = False
SERVICE_BASE_URL = 'http://fakeapi.net'
NUMBER_OF_REQUEST_RETRIES = 1
