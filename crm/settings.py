"""
Django settings for OneKloud CRM project.

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

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    '127.0.0.1'
]

AUTH_USER_MODEL = 'accounts.User'


# Django application definition
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)


# Third-party application definition
INSTALLED_APPS += (
    'south',
)


# OneKloud CRM application definition
INSTALLED_APPS += (
    'crm.apps.accounts',
    'crm.apps.core',
    'crm.apps.events',
    'crm.apps.companies',
    'crm.apps.customers',
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


# OneKloud CRM application definition
MIDDLEWARE_CLASSES += (
    'crm.apps.core.middleware.PermissionMiddleware',
)


# Django context processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.media',
    'django.contrib.messages.context_processors.messages',
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


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


# Test settings
if 'test' in sys.argv:
    from crm.settings_test import *
