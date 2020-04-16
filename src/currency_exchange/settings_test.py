from currency_exchange.settings import *


DEBUG = False

ALLOWED_HOSTS = ['*']


CELERY_ALWAYS_EAGER = CELERY_TASK_ALWAYS_EAGER = True


STATIC_ROOT = os.path.join(BASE_DIR, '..', "static_content", 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
'default': {
'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
}
}