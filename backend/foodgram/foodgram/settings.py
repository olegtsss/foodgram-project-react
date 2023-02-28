import os
from datetime import timedelta
from pathlib import Path

# from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '!9(xta)jr8n5bpom#$7q3osx(9g6nn(ra06y!g%7wr3mdr(wp+'
DEBUG = True
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',
    'recipes.apps.RecipesConfig',
    'rest_framework',
    'django_filters',
    'rest_framework.authtoken',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'foodgram.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
WSGI_APPLICATION = 'foodgram.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
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
LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
MEDIA_URL = 'http://localhost:8000/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
AUTH_USER_MODEL = 'recipes.User'

# Максимальная длина адреса электронной почты
MAX_LENGTH_EMAIL = 254
# Максимальная длина имени
MAX_LENGTH_FIRSTNAME = 150
# Максимальная длина фамилии
MAX_LENGTH_LASTNAME = 150
# Максимальная длина пароля
MAX_LENGTH_PASSWORD = 150
# Максимальная длина имени тега
MAX_LENGTH_TAG_NAME = 10
# Максимальная длина для HEX кода цвета тега
MAX_LENGTH_TAG_COLOR = 10
# Максимальная длина слага для тега
MAX_LENGTH_TAG_SLUG = 10
# Максимальная длина имени ингридиента
MAX_LENGTH_INGREDIENT_NAME = 128
# Максимальная длина имени единицы измерения ингридиента
MAX_LENGTH_INGREDIENT_UNIT = 24
# Максимальная длина имени рецепта
MAX_LENGTH_RECIPE_NAME = 200
# Минимальное время приготовления рецепта (в минутах)
MIN_COOKING_TIME = 1
# Максимальное время приготовления рецепта (в минутах)
MAX_COOKING_TIME = (60 * 24 * 7)
# Сообщение для некорректно указанного времени приготовления
COOKING_TIME_MESSAGE = 'Указано не корректное время приготовления.'
# Минимальное количество ингридиента в рецепте
MIN_INGREDIENT_COUNT = 0
# Максимальное количество ингридиента в рецепте
MAX_INGREDIENT_COUNT = 999999999
# Сообщение для некорректно указанного количества ингридиента
INGREDIENT_COUNT_MESSAGE = 'Указано не корректное количество.'

# Работа с токенами
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    #'DEFAULT_FILTER_BACKENDS': [
    #    'django_filters.rest_framework.DjangoFilterBackend',
    #],
}
