"""
Django settings for bookstore_project project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os 
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ENVIRONMENT = 'production'
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv('SECRET_KEY'))

# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ("web-production-b540.up.railway.app", "127.0.0.1","localhost")

# production

if ENVIRONMENT == 'production':
    DEBUG = False
    SECURE_BROWSER_XSS_FILTER = True # new
    X_FRAME_OPTIONS = 'DENY' # new
    SECURE_SSL_REDIRECT = True # new
    SECURE_HSTS_SECONDS = 3600 # new
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True # new
    SECURE_HSTS_PRELOAD = True # new
    SECURE_CONTENT_TYPE_NOSNIFF = True # new
    SESSION_COOKIE_SECURE = True # new
    CSRF_COOKIE_SECURE = True # new
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
else:
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',# new
    'django.contrib.staticfiles',
    'django.contrib.sites', # new

    # Third-party
    'crispy_forms', # new
    'allauth', # new
    'allauth.account', # new
    'debug_toolbar',
    'crispy_bootstrap4',
    'django_celery_results',
    'django_celery_beat',
    # Local
    'mainlobby.apps.MainlobbyConfig',
    'users.apps.UsersConfig',
]   

# django-allauth config
LOGIN_REDIRECT_URL = 'home'
ACCOUNT_LOGOUT_REDIRECT = 'home' # new
SITE_ID = 1
AUTHENTICATION_BACKENDS = (
'django.contrib.auth.backends.ModelBackend',
'allauth.account.auth_backends.AuthenticationBackend',
)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
ACCOUNT_USERNAME_REQUIRED = False # new
ACCOUNT_AUTHENTICATION_METHOD = 'email' # new
ACCOUNT_EMAIL_REQUIRED = True # new
ACCOUNT_UNIQUE_EMAIL = True # new



# django-crispy-forms
CRISPY_TEMPLATE_PACK = 'bootstrap4' # new
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware', # new
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # new
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware', # new
]

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 604800
CACHE_MIDDLEWARE_KEY_PREFIX = ''

ROOT_URLCONF = 'datamagnum.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')], # new
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'datamagnum.wsgi.application'



if ENVIRONMENT == 'production':
    DATABASES = {
        'default': {
            #'ENGINE': 'django.db.backends.sqlite3',
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'railway',
            'USER': 'postgres',
            'PASSWORD': 'i43hlLrgvg24P3RD3wKi',
            'HOST': 'containers-us-west-41.railway.app',
            'PORT': '5939',
        }
    }
else:
    DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "mydatabase",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/' 
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.CustomUser' 



# django-debug-toolbar
import socket
hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
INTERNAL_IPS = [ip[:-1] + "1" for ip in ips]


# CELERY SETTINGS

CELERY_BROKER_URL = 'redis://web-production-b540.up.railway.app:6379/0'
accept_content = ['application/json']
result_serializer = 'json'
task_serializer = 'json'
timezone = 'UTC'

result_backend = 'django-db'

#CELERY BEAT
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# SMTP Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtppro.zoho.eu'
EMAIL_USE_SSL = True
EMAIL_PORT = 465
EMAIL_HOST_USER = 'support@valoriado.com'
EMAIL_HOST_PASSWORD = 'SRHYxJF6fqhd'
DEFAULT_FROM_EMAIL = 'support@valoriado.com'

# Stripe

if ENVIRONMENT == 'production':
    STRIPE_PUBLIC_KEY = 'pk_live_51Mbox2IQDkGdDbUYbS6zMb7j65uZuWgrp3Oqdskf1tOS9XgGoqPggVD0IPWBU6cihKugl5N4rJym2MIi5K5B652i00Zx8YTxUJ'
    STRIPE_API_KEY = str(os.getenv('STRIPE_API_KEY'))
else:
    TEST_STRIPE_PUBLIC_KEY = 'pk_test_51Mbox2IQDkGdDbUYvfjf4ItvBDZI4ZMA5Ic6XJnytAEZG1mwkR7J0Jc1Zo2xpDMBX4FqKi1aANHsQa8eFgRbpldt00JYckHaYg'
    TEST_STRIPE_API_KEY = 'sk_test_51Mbox2IQDkGdDbUYJBAuX34hyASJqjpvYYHyDGo7nOyWLG5jlvctEGMhxbGW7oVfYlwVoljqMo0MoLfhTNP0MhKM00My1cOU7W'


STRIPE_SIGNING_SECRET = 'whsec_0d01203d265aaaa06ec4d6de76105a45f84e35cb5f2da3103bfa0479509295b9'

MEDIA_ROOT = os.path.join(BASE_DIR,'media')
MEDIA_URL = '/media/'

