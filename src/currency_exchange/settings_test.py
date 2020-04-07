from currency_exchange.settings import *


DEBUG = False

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'qmzrjf123@gmail.com'
EMAIL_HOST_PASSWORD = 'BS8xYbtUW3'

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