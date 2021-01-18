"""
Django settings for ghaza project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import dj_database_url
import os


try:
    from . import secret
except ImportError:
    pass

try:
    SECRET_KEY = secret.SECRET_KEY
except NameError:
    SECRET_KEY = os.getenv('SECRET_KEY', None)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!


# SECURITY WARNING: don't run with debug turned on in production!

ALLOWED_HOSTS = ['127.0.0.1']

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
# Application definition

INSTALLED_APPS = [
    # 3rd party packages
    'bootstrap4',
    'crispy_forms',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # own apps
    'food',
    'TodoApp',
    'zarinpal',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ghaza.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'ghaza.wsgi.application'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)
# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

AUTH_USER_MODEL = 'food.SiteUser'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

SITE_ID = 2

LOGIN_REDIRECT_URL = '/ghaza/'

LOGIN_URL = "/ghaza/login/"

import django_heroku
django_heroku.settings(locals())

if os.environ.get('DEBUG') == 'TRUE':
    DEBUG = True
elif os.environ.get('DEBUG') == 'FALSE':
    DEBUG = False
else:
    DEBUG = True

if os.environ.get('ZARINPAL_MAIN_URL'):
    ZARINPAL_MAIN_URL = os.environ.get('ZARINPAL_MAIN_URL')
else:
    ZARINPAL_MAIN_URL = 'http://localhost:8000'

if os.environ.get('ZARINPAL_SANDBOX') == False:
    ZARINPAL_SANDBOX = False
else:
    ZARINPAL_SANDBOX = True # Defaults to true

if os.environ.get('GOOGLE_KEY'):
    SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get('GOOGLE_KEY')
else:
    try:
        SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = secret.GOOGLE_KEY
    except ImportError:
        pass

if os.environ.get('GOOGLE_SECRET'):
    SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get('GOOGLE_SECRET')
else:
    try:
        SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = secret.GOOGLE_SECRET
    except ImportError:
        pass

PROJECT_ROOT = os.path.join(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')

STATICFILES_DIRS = (
    os.path.join(PROJECT_ROOT, 'static'),
)

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

prod_db  =  dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(prod_db)