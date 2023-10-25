import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    'SECRET_KEY',
    default='django-insecure-d$4*vp6zvq0y-7vr0^w1@!r0*bd4hh9lgsp_y$7s%-f3y9wd8c'
)

DEBUG = os.getenv(
    'DEBUG',
    default='False',
) == 'True'

ALLOWED_HOSTS = os.getenv(
    'ALLOWED_HOSTS',
    default='127.0.0.1 localhost',
).split()

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework.authtoken',
    'rest_framework',
    'djoser',
    'django_filters',
    'colorfield',
]

PROJECT_APPS = [
    'users.apps.UsersConfig',
    'api.apps.ApiConfig',
    'recipes.apps.RecipesConfig',
    'obsceneLang.apps.ObscenelangConfig',
    'core.apps.CoreConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

# postgresql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'django'),
        'USER': os.getenv('POSTGRES_USER', 'mastermind'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'password'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', 5432),
    }
}

# sqlite3
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'collected_static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

PAGE_COUNT = 6
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': PAGE_COUNT,
}

DJOSER = {
    "LOGIN_FIELD": "email",
    'SERIALIZERS': {
        'user_create': ('api.serializers.'
                        'users_serializers.UserSignUpSerializer'),
        'user': 'api.serializers.users_serializers.UserSerializer',
        'current_user': 'api.serializers.users_serializers.UserSerializer',
    },
    'PERMISSIONS': {
        'user': ['djoser.permissions.CurrentUserOrAdminOrReadOnly'],
        'user_list': ['rest_framework.permissions.AllowAny'],
    },
    'HIDE_USERS': False,
}

USERNAME_MAX_LENGTH = 150  # Максимальный размер логина
WORD_MAX_LENGTH = 50  # Максимальный размер слова
COMMENTS_MAX_LENGTH = 75  # Максимальный размер комментария
THRESHOLD = 2  # Порог для расстояния Левенштейна
EMAIL_MAX_LENGTH = 254  # Максимальный размер email
SLUG_MAX_LENGTH = 200  # Максимальный размер slug
FIRSTNAME_MAX_LENGTH = 150  # Максимальный размер имени
TAGNAME_MAX_LENGTH = 200  # Максимальный размер названия тега
LASTNAME_MAX_LENGTH = 150  # Максимальный размер фамилии
MIN_VALUE = 1  # Минимальное кол-во времени или кол-во ингредиента
COLOR_CODE_MAX_LENGTH = 7  # Максимальный размер цветового кода
ROLE_MAX_LENGTH = 20  # Максимальный размер названия роли
INGREDIENT_NAME_MAX_LENGTH = 200  # Максимальный размер ингредиента
MEASUREMENT_UNIT_MAX_LENGTH = 200  # Максимальный размер единицы измерения
RECIPE_NAME_MAX_LENGTH = 200  # Максимальный размер названия рецепта
CSV_FOLDER = f"{BASE_DIR}/static/data/"  # Расположение csv файлов

CSRF_TRUSTED_ORIGINS = ['https://myfoodgram.ddns.net', ]
