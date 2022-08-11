"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""
import os
from datetime import timedelta

import environ

from pathlib import Path

from firebase_admin import initialize_app

env = environ.Env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')


ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = True

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

}


INSTALLED_APPS = [
    'modeltranslation',
    'jet.dashboard',
    'jet',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',

    # Library
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'django_filters',
    'oauth2_provider',
    'social_django',
    'rest_framework_social_oauth2',
    'crispy_forms',
    'rest_framework_simplejwt.token_blacklist',
    'fcm_django',

    # Apps
    'src.user',
    'src.scooter',
    'src.bicycle',
    'src.cart',
    'src.order',
    'src.payment',
    'src.notification',
    'src.wallets.paybox_wallets',
    'src.wallets.stripe_wallets',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'
LOGIN_URL = '/login/'

SITE_ID = 2

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES_URL = 'templates'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_URL],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
#
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT')
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'scooter_bicycle3',
#         'USER': 'murat4',
#         'PASSWORD': 'neymarjunior23',
#         'HOST': 'localhost',
#         'PORT': '5432'
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'user.User'


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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Asia/Bishkek'

USE_I18N = True

USE_TZ = True

gettext = lambda s: s
LANGUAGES = (
    ('ru', gettext('Russia')),
    ('en', gettext('English')),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = 'media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'assets/static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'assets/media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
CACHE_TTL = 60 * 1


EMAIL_BACKEND = env('EMAIL_BACKEND')
EMAIL_USE_TLS = env('EMAIL_USE_TLS')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_PORT = env('EMAIL_PORT')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')

REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')
CELERY_BROKER_URL = env('CELERY_BROKER_URL')
CELERY_BROKER_TRANSPORT = env('CELERY_BROKER_TRANSPORT')
CELERY_TIMEZONE = env('CELERY_TIMEZONE')
CELERY_TASK_TRACK_STARTED = env('CELERY_TASK_TRACK_STARTED')
CELERY_TASK_TIME_LIMIT = 10 * 60
CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')

SOCIAL_AUTH_POSTGRES_JSONFIELD = env('SOCIAL_AUTH_POSTGRES_JSONFIELD')

AUTHENTICATION_BACKENDS = (
    'social_core.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
)


SOCIAL_AUTH_GITHUB_KEY = env('SOCIAL_AUTH_GITHUB_KEY')
SOCIAL_AUTH_GITHUB_SECRET = env('SOCIAL_AUTH_GITHUB_SECRET')

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

TWILIO_ACCOUNT_SID = env("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = env("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = env("TWILIO_NUMBER")

PAYBOX_PROJECT_ID = env.str('PAYBOX_PROJECT_ID')
PAYBOX_SECRET_KEY = env.str('PAYBOX_SECRET_KEY')
PAYBOX_SALT = env.str('PAYBOX_SALT')
PAYBOX_SUCCESS_URL_METHOD = env.str('PAYBOX_SUCCESS_URL_METHOD')
PAYBOX_CURRENCY = env.str('PAYBOX_CURRENCY')
PAYBOX_LANGUAGE = env.str('PAYBOX_LANGUAGE')
PAYBOX_URL = env.str(
    'PAYBOX_URL'
)
PAYBOX_SUCCESS_URL = env.str(
    'PAYBOX_SUCCESS_URL'
)
PAYBOX_RESULT_URL = env.str(
    'PAYBOX_RESULT_URL'
)

ADMINS = (
    (env('ADMINS_PHONE_NUMBER'), env('ADMINS_USERNAME'), env('ADMINS_EMAIL'),
     env('ADMINS_FIRST_NAME'), env('ADMINS_LAST_NAME'), env('ADMINS_PASSWORD')),
)

STRIPE_PUBLISH_KEY = env('STRIPE_PUBLISH_KEY')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_WEBHOOK_SECRET_KEY = env('STRIPE_WEBHOOK_SECRET_KEY')

SITE_URL = env('SITE_URL')

APPEND_SLASH = False

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=14),
    'AUTH_HEADER_TYPES': ('Bearer', 'JWT'),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s:%(module)s:%(lineno)d:%(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
        },
    },
    'loggers': {
        'mailings': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        }
    },
}

CSRF_COOKIE_SECURE = True

FIREBASE_API_KEY = env('FIREBASE_API_KEY')

FIREBASE_APP = initialize_app()

FCM_DJANGO_SETTINGS = {
    "APP_VERBOSE_NAME": "My APP",
    "FCM_SERVER_KEY": env("FCM_SERVER_KEY"),
    "ONE_DEVICE_PER_USER": False,
    "DELETE_INACTIVE_DEVICES": True,
    "UPDATE_ON_DUPLICATE_REG_ID": True,
}
