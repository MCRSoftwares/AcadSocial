# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Sistema: 1.0.0a007
Versão do Código: 01v006a

Responsável: Victor Ferraz
Auxiliar: Alessandro Henrique, Avyner Lucena, Elson Rodrigues, José Durval

Requisito(s): -
Caso(s) de Uso: -

Descrição:
    Configuração geral do sistema AcadSocial.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p00wlkr%hi55$beo%x*m2ut$@)3mtiq98kbxe_a568$*iq4q=5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = []

SYSTEM_HOST = '127.0.0.1:8000'

LANGUAGE_CODE = 'pt-br'

LANGUAGES = (
    ('pt-br', u'Português'),
    ('en-us', u'Inglês'),
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'mainAcad',
    'contas',
    'grupos',
    'universidades',
)

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
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

ROOT_URLCONF = 'AcadSocial.urls'

WSGI_APPLICATION = 'AcadSocial.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

TIME_ZONE = 'America/Recife'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static & Media files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
# DEBUG ONLY

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

AWS_S3_SECURE_URLS = False       # use http instead of https
AWS_QUERYSTRING_AUTH = False     # don't add complex authentication-related query parameters for requests
AWS_S3_ACCESS_KEY_ID = '<keyid>'     # enter your access key id
AWS_S3_SECRET_ACCESS_KEY = '<secretkey>' # enter your secret access key
AWS_STORAGE_BUCKET_NAME = 'acadsocial'
AWS_S3_CUSTOM_DOMAIN = 's3-sa-east-1.amazonaws.com/%s' % AWS_STORAGE_BUCKET_NAME
STATIC_URL = "http://%s/" % AWS_S3_CUSTOM_DOMAIN
MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

# Templates

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

# Custom User Model

AUTH_USER_MODEL = 'contas.UsuarioModel'

LOGIN_URL = '/conta/login/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'AcadSocial@gmail.com'
EMAIL_HOST_PASSWORD = 'aaedv2015'
EMAIL_PORT = 587
SERVER_EMAIL = 'AcadSocial <AcadSocial@gmail.com>'
DEFAULT_FROM_EMAIL = 'AcadSocial <AcadSocial@gmail.com>'
