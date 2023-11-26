import logging
from pathlib import Path

import environ
from django.utils.translation import gettext_lazy as _

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
LOCALE_PATHS = [str(BASE_DIR / 'locale')]

# Log Reports
logging.basicConfig(filename='stderr.log', level=logging.ERROR)

# Environment config
env = environ.Env(
    environment=(str, 'local'),
    SECRET_KEY=(str, 'g!d7f04nkzp4n#*3ds5dci5qw248zr146wt6vu)i&bpzwqz@9bfvw90'),
    ALLOWED_HOSTS=(list, ['127.0.0.1', 'localhost']),
    LANGUAGE_CODE=(str, 'en-us'),
    TIME_ZONE=(str, 'America/Bogota'),
    DB_NAME=(str, 'app_core'),
    DB_USER=(str, 'app_core'),
    DB_PASSWORD=(str, 'app_core'),
    DB_HOST=(str, 'localhost'),
    DB_PORT=(int, 5432),
    DB_CONN_MAX_AGE=(int, 60),
    DB_CHARSET=(str, 'UTF8'),
    EMAIL_BACKEND=(str, 'django.core.mail.backends.smtp.EmailBackend'),
    DEFAULT_FROM_EMAIL=(
        str, 'Django all in one project <noreply@sebasmoralesd.com>'
    ),
    SERVER_EMAIL=(str, 'noreply@sebasmoralesd.com'),
    EMAIL_SECURITY_CONNECTION=(str, 'TLS'),
    EMAIL_PORT=(int, 587),
    EMAIL_TIMEOUT=(int, 300),
    EMAIL_HOST_USER=(str, 'noreply@sebasmoralesd.com'),
    EMAIL_HOST_PASSWORD=(str, 'email_password123@*'),
    ADMIN_URL=(str, 'admin/'),
    CELERY_BROKER_URL=(str, 'redis://127.0.0.1:6379'),
    DJANGO_ADMIN_FORCE_ALLAUTH=(bool, True),
    DJANGO_ACCOUNT_ALLOW_REGISTRATION=(bool, True),
    CORS_ORIGIN_WHITELIST=(list, ['http://localhost:3000']),
    DOMAIN=(str, 'localhost'),
    ERROR_TEMPLATE=(str, 'error_template.html'),
    INTERNAL_IPS=(list, ['localhost', '127.0.0.1', '0.0.0.0'])
)
environ.Env.read_env((BASE_DIR / '.env'))
environment = env(
    'environment'
)

# Security
if environment.lower() in ['local', 'qa']:
    DEBUG = True
else:
    DEBUG = False
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'

# Django secret key
SECRET_KEY = env(
    'SECRET_KEY'
)

# Django internationalization
LANGUAGE_CODE = env(
    'LANGUAGE_CODE'
)
TIME_ZONE = env(
    'TIME_ZONE'
)
LANGUAGES = [
    ('es', _('Spanish')),
    ('en', _('English'))
]
USE_I18N = True
USE_TZ = True

# Allowed Hosts
ALLOWED_HOSTS = env.list(
    'ALLOWED_HOSTS'
)
INTERNAL_IPS = env.list(
    'INTERNAL_IPS'
)

# Apps
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.postgres',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles'
]
THIRD_PUBLIC_APPS = [
    'auditlog',
    'corsheaders',
    'debug_toolbar',
    'django_extensions',
    'import_export'
]
CUSTOM_PUBLIC_APPS = [
    'apps.public_apps.errors',
    'apps.public_apps.users',
    'apps.public_apps.utils',
]
CUSTOM_TENANT_APPS = [
    'apps.tenant_apps.alarms',
    'apps.tenant_apps.clients',
]

CUSTOM_APPS = [
    # Change the name of this variable affects the utils app delete_migrations command
    *CUSTOM_PUBLIC_APPS,
    *CUSTOM_TENANT_APPS
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PUBLIC_APPS + CUSTOM_PUBLIC_APPS + CUSTOM_TENANT_APPS
SITE_ID = 1
DOMAIN = env(
    'DOMAIN'
)

# Middleware
MIDDLEWARE = [
    # 'django_tenants.middleware.main.TenantMainMiddleware', TODO django_tenants Middleware
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # 'whitenoise.middleware.WhiteNoiseMiddleware', TODO whitenoise Middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'auditlog.middleware.AuditlogMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'allauth.account.middleware.AccountMiddleware' TODO allauth Middleware
]

# Url config
ROOT_URLCONF = 'app_core.urls_public'
ADMIN_URL = env(
    'ADMIN_URL'
)

# Templates config
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'app_core' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'apps.public_apps.utils.context_processors.custom_processors'
            ],
        },
    },
]
ERROR_TEMPLATE = env(
    'ERROR_TEMPLATE'
)

# Server Gateway Interface
ASGI_APPLICATION = 'app_core.asgi.application'

# Database config
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
        'CONN_MAX_AGE': env('DB_CONN_MAX_AGE'),
        'CHARSET': env('DB_CHARSET'),
        'ATOMIC_REQUESTS': True
    }
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Auth
AUTH_USER_MODEL = 'users.UserModel'
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'apps.public_apps.utils.backend.EmailOrUsernameModelBackend',
]
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

# Static & Media ROOT
STATIC_ROOT = str(BASE_DIR / 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [str(BASE_DIR / 'app_core' / 'static')]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]
MEDIA_ROOT = str(BASE_DIR / 'app_core' / 'media')
MEDIA_URL = "/media/"

# Rest
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': True,
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
    }
}
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ]
}

# Email config
EMAIL_BACKEND = env(
    'EMAIL_BACKEND'
)
EMAIL_TIMEOUT = env(
    'EMAIL_TIMEOUT'
)
DEFAULT_FROM_EMAIL = env(
    'DEFAULT_FROM_EMAIL'
)
SERVER_EMAIL = env(
    'SERVER_EMAIL'
)
EMAIL_SECURITY_CONNECTION = env(
    'EMAIL_SECURITY_CONNECTION'
)
EMAIL_PORT = env(
    'EMAIL_PORT'
)
EMAIL_TIMEOUT = env(
    'EMAIL_TIMEOUT'
)
EMAIL_HOST_USER = env(
    'EMAIL_HOST_USER'
)
EMAIL_HOST_PASSWORD = env(
    'EMAIL_HOST_PASSWORD'
)

# Utils
GRAPH_MODELS = {
    'all_applications': True,
    'group_models': True,
}
