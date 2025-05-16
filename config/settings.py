import os
from pathlib import Path
import dj_database_url

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Безопасность
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-dev-key')
DEBUG = os.environ.get('DEBUG', '') != 'False'
ALLOWED_HOSTS = ['trend-production.up.railway.app', '127.0.0.1', 'localhost']

# Приложения проекта
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Наши приложения
    'apps.users',
    'apps.products',
    'apps.orders',
    'apps.cart',
    'apps.core',
    'cloudinary',
    'cloudinary_storage',
]

JAZZMIN_SETTINGS = {
    "site_title": "TRENDFORU",
    "site_header": "Админпанель",
    "site_brand": "TRENDFORU",
    "welcome_sign": "Добро пожаловать 👋",
    "copyright": "Dark UI © 2025",
    "search_model": ["products.Product", "users.Profile"],

    "topmenu_links": [
        {"name": "На сайт", "url": "/", "permissions": ["auth.view_user"]},
    ],

    "icons": {
        "auth.user": "fas fa-user-circle",
        "auth.Group": "fas fa-users-cog",
        "products.Product": "fas fa-box-open",
        "products.Category": "fas fa-layer-group",
        "orders.Order": "fas fa-receipt",
        "cart.CartItem": "fas fa-shopping-bag",
    },

    "hide_apps": [],
    "show_sidebar": True,
    "navigation_expanded": True,
    "default_icon_parents": "fas fa-moon",
    "default_icon_children": "fas fa-circle",

    "related_modal_active": True,
    "use_google_fonts_cdn": True,
    "custom_css": "admin/css/dark_theme.css",
    "custom_js": None,
    "show_ui_builder": False,
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dp6jechuq',
    'API_KEY': '942447165995487',
    'API_SECRET': 'uGL-HQ4cK2obQRLEVAW58aY7_Ps',
    'SECURE': True
}
# Middleware
# MIDDLEWARE = [
#     'django.middleware.security.SecurityMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

# База данных
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:HdcRXWBNnBhKlKKvVjOtyzROpuJWAgcQ@switchback.proxy.rlwy.net:15085/railway'
    )
}
# Авторская модель пользователя
AUTH_USER_MODEL = 'users.User'

# Пароли
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
]

# Язык и таймзона
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True
CSRF_TRUSTED_ORIGINS = ['https://trend-production.up.railway.app']

# Статика и медиа
# STATIC_URL = '/static/'
# STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

# По умолчанию
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Django settings here

