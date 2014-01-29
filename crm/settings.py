"""
Django settings for Onekloud CRM project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(__file__)

# Adding system paths
import sys
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, 'apps'))
sys.path.append(os.path.join(BASE_DIR, 'lib'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/dev/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9gfi8y+so)y+51=b@xpfnnlkm9^g+#xgjnl%sycs_n!5y)pvnz'

# SECURITY WARNING: don't reveal this salt!
ACTIVATION_SALT = 'af9df61ea6dc9a73439794d9d46afe1e376ae9983255e85b46c83123478'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    '37.139.24.123',
    '.onekloud.com'
]

AUTH_USER_MODEL = 'accounts.User'

ADMINS = (
    ('Aldash Biibosunov', 'support@onekloud.com'),
)

LOGIN_URL = 'accounts:login'


# Django application definition
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
)


# Third-party application definition
INSTALLED_APPS += (
    'south',
)


# Onekloud CRM application definition
INSTALLED_APPS += (
    'crm.apps.accounts',
    'crm.apps.core',
    'crm.apps.events',
    'crm.apps.customers',
    'crm.apps.reports',
)


# Django middleware classes
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


# Onekloud CRM middleware definition
MIDDLEWARE_CLASSES += (
    'crm.apps.core.middleware.PermissionMiddleware',
    'crm.apps.core.middleware.RedirectMiddleware',
)


# Django context processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
)


# Onekloud CRM context processors definition
TEMPLATE_CONTEXT_PROCESSORS += (
    'apps.core.context_processors.tour',
    'apps.accounts.context_processors.users',
)


ROOT_URLCONF = 'crm.urls'

WSGI_APPLICATION = 'crm.wsgi.application'


# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'crm',
        'USER': 'crmuser',
        'PASSWORD': 'vivendi89',
        'HOST': 'localhost',
        'PORT': '5432'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/dev/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kuala_Lumpur'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/dev/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, '../static/')

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'common_static'),
)


# Template directories
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)


# Email
EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = 'aldash@onekloud.com'

EMAIL_HOST_PASSWORD = 'Vivendi89!'

EMAIL_PORT = 587

EMAIL_USE_TLS = True


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, '../logs/error.log')
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True
        }
    }
}


# New Relic
NEW_RELIC_KEY = '26774c5c18c72e10cefbe031a75e0d427b714945'


# Celery settings
BROKER_URL = '127.0.0.1'

BROKER_PORT = 5672

BROKER_USER = 'celery'

BROKER_PASSWORD = 'vivendi89'

BROKER_VHOST = 'crm'

CELERY_BACKEND = 'amqp'

CELERY_RESULT_DBURI = ''


# Dev settings
try:
    from crm.settings_local import *
except ImportError:
    pass


# Test settings
if 'test' in sys.argv:
    from crm.settings_test import *
