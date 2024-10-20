import os
from datetime import timedelta
from pathlib import Path
import logging.config
from decouple import config
from corsheaders.defaults import default_headers

BASE_DIR = Path(__file__).resolve().parent.parent


DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'#config('DEFAULT_FILE_STORAGE')
AWS_ACCESS_KEY_ID = 'minioadmin'#config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = 'minioadmin'#config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'telegram'#config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = 'http://minio:9000'
AWS_S3_FILE_OVERWRITE = False
AWS_LOCATION = 'static'

RABBIT_HOST = 'localhost'#config('RABBIT_HOST')
RABBIT_QUEUE = 'hello'#config('RABBIT_QUEUE')
RABBIT_QUEUE_SEND = 'hello'#config('RABBIT_QUEUE_SEND')
RABBIT_ROUTING_KEY = 'hello'#config('RABBIT_ROUTING_KEY')

BOT_TOKEN = '6880396170:AAEi9ZWvprUuHSXy1qTFzPG0mx5Sy9Md5Dw'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-8r+5(vc7yu@k5a_p4k(!xwex%#0+9xxh!u8+zp+z88+mgrlb!e',
)

DEBUG = True#getenv('DJANGO_DEBUG', '0') == "1"

ALLOWED_HOSTS = [
    "*",
    "127.0.0.1",
    "0.0.0.0"
] + config("DJANGO_ALLOWED_HOSTS", "").split(",")


AUTH_USER_MODEL = 'auth.User'


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.staticfiles",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.postgres",
    #my app
    "profile",
    "users",
    "application",
    #plugins
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework.authtoken',
    'corsheaders',
]

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_currentuser.middleware.ThreadLocalUserMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "Help_dasks.urls"

#CORS_ALLOW_HEADERS = [
#    'Authorization',
#]

CORS_ALLOW_ALL_ORIGINS = True

#CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]

#CORS_TRUSTED_ORIGINS = ["http://localhost:3000"]

#CORS_ALLOW_HEADERS = (
#    'Access-Control-Allow-Headers',
#    'Access-Control-Allow-Credentials',
#)

#CORS_ALLOW_METHODS = [
#    'DELETE',
#    'GET',
#    'OPTIONS',
#    'PATCH',
#    'POST',
#    'PUT',
#]

# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:3000',
# ]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        #'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
            # 'rest_framework.permissions.IsAuthenticated',
        ],
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = "Help_dasks.wsgi.application"

LOGIN_REDIRECT_URL = '/../app/aplications-list'
LOGOUT_REDIRECT_URL = "login"

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': 'db_helpDesk',
       'USER': 'postgres',
       'PASSWORD': 'root',
       'HOST': "postgres",
       'PORT': '5432',
   }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

#STATICFILES_DIRS = [
#   os.path.join(Path(__file__).resolve().parent.parent, "static"),
#]

STATIC_ROOT=os.path.join(BASE_DIR, "/static/")

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), ]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

#DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

