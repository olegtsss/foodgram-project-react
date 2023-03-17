import os

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.getenv('SECRET_KEY', default='secret_key')
DEBUG = os.getenv('DEBUG', default=False)
ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS', default='*')]
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Приложение users
    'users.apps.UsersConfig',
    # Приложение api
    'api.apps.ApiConfig',
    # Приложение recipes
    'recipes.apps.RecipesConfig',
    # Приложение для проверки принадлежности email пользователю
    'emailcheck.apps.EmailcheckConfig',
    'rest_framework',
    'corsheaders',
    'django_filters',
    'rest_framework.authtoken',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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

if os.getenv('NEED_SQLITE'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': os.getenv(
                'DB_ENGINE', default='django.db.backends.postgresql'),
            'NAME': os.getenv('POSTGRES_DB', default='postgres'),
            'USER': os.getenv('POSTGRES_USER', default='postgres'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
            'HOST': os.getenv('DB_HOST', default='db'),
            'PORT': os.getenv('DB_PORT', default=5432)
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
# Для работы Docker указать STATIC_ROOT и создать папку static
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)
MEDIA_URL = '/media/'
# MEDIA_URL = 'http://localhost:8000/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
AUTH_USER_MODEL = 'users.User'
# Работа REST
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.ScopedRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'low_request': '1/minute',
    }
}
# CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOWED_ORIGINS = [
    'https://localhost',
    'https://127.0.0.1'
]
CORS_URLS_REGEX = r'^/api/.*$'

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
# Ограничение для работы пагинатора CustomPagination
PAGE_SIZE = 50

# SMTP backend
if os.getenv('SMTP_BACKEND_EMULATION'):
    # Backend для эмуляции почтового сервера
    EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
    # Директория для писем при эмуляции
    EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'sent_emails')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')

# Emailcheck application:
URL_FOR_EMAIL_VERIFICATION = os.getenv(
    'URL_FOR_EMAIL_VERIFICATION', default='http://127.0.0.1:8000')
