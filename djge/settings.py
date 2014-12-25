"""
djge/settings.py
"""
import os
import djgesettings
from django.conf import global_settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = djgesettings.SECRET_KEY
DEBUG = djgesettings.DEBUG
TEMPLATE_DEBUG = DEBUG
ALLOWED_HOSTS = djgesettings.ALLOWED_HOSTS


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'encounter',
    'inventory',
    'mobile',
    'player',
    'world',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.open_id.OpenIdAuth',
    'social.backends.twitter.TwitterOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

ROOT_URLCONF = 'djge.urls'

WSGI_APPLICATION = 'djge.wsgi.application'

DATABASES = djgesettings.DATABASES

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, '_static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, '_templates'),
    )

TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'django.core.context_processors.request',
)
