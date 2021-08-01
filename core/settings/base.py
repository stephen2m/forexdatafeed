from os.path import join
from pathlib import Path

import environ
import structlog
from celery.schedules import crontab
from configurations import Configuration, values

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


class BaseConfiguration(Configuration):
    # Environment
    env = environ.Env()
    DOTENV = join(BASE_DIR, '../.env')
    print(f'base dir is {BASE_DIR}')
    print(f"{join(BASE_DIR, '../.env')}")

    DEBUG = env.bool('DJANGO_DEBUG', default=False)

    # https://docs.djangoproject.com/en/3.2/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ['*']

    # https://docs.djangoproject.com/en/3.2/ref/settings/#secret-key
    SECRET_KEY = env('DJANGO_SECRET_KEY')

    # Apps
    LOCAL_APPS = [
        'apps.forex.apps.Forex',
    ]

    THIRD_PARTY_APPS = []

    DJANGO_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]

    # https://docs.djangoproject.com/en/3.2/ref/settings/#installed-apps
    INSTALLED_APPS = LOCAL_APPS + THIRD_PARTY_APPS + DJANGO_APPS

    # https://docs.djangoproject.com/en/3.2/ref/settings/#middleware
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [BASE_DIR / 'templates'],
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

    ROOT_URLCONF = 'core.urls'

    WSGI_APPLICATION = 'core.wsgi.application'

    DATABASES = {
        # Raises ImproperlyConfigured exception if DATABASE_URL not in os.environ
        'default': env.db(default='postgres://postgres:@postgres:5432/postgres')
    }

    # Password validation
    # https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
    # https://docs.djangoproject.com/en/3.2/topics/i18n/
    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    # https://docs.djangoproject.com/en/3.2/ref/settings/#use-tz
    USE_TZ = True

    # https://docs.djangoproject.com/en/3.2/ref/settings/#use-i18n
    USE_I18N = True

    # https://docs.djangoproject.com/en/3.2/ref/settings/#use-l10n
    USE_L10N = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/3.2/howto/static-files/
    STATIC_URL = '/static/'

    # Default primary key field type
    # https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    CELERY_BROKER_URL = env('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = env('CELERY_RESULT_BACKEND')

    CELERY_BEAT_SCHEDULE = {
        'fetch_latest_forex_data': {
            'task': 'apps.forex.tasks.update_forex_data',
            'schedule': crontab(minute=0, hour='*/1'),
        },
    }

    CELERY_IMPORTS = ('apps.forex.tasks',)

    if USE_TZ:
        CELERY_TIMEZONE = TIME_ZONE

    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt='iso'),
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(encoding='utf-8', errors='backslashreplace'),
            structlog.processors.ExceptionPrettyPrinter(),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=structlog.threadlocal.wrap_dict(dict),
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    pre_chain = [
        # Add the log level and a timestamp to the event_dict if the log entry
        # is not from structlog.
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt='iso'),
    ]

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                '()': structlog.stdlib.ProcessorFormatter,
                'processor': structlog.processors.JSONRenderer(sort_keys=True),
                'foreign_pre_chain': pre_chain,
            },
        },
        'handlers': {
            'default': {'class': 'logging.StreamHandler', 'formatter': 'default', 'level': 'INFO'},
        },
        'loggers': {
            'api_requests': {'handlers': ['default'], 'level': 'INFO', 'propagate': False},
        },
    }

    API_KEY = values.Value('API_KEY')
    ALPHAVANTAGE_API_KEY = values.Value('ALPHAVANTAGE_API_KEY')
