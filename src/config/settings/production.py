from dotenv import load_dotenv

import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

# reading ./deployment/.env file
load_dotenv(os.path.join(BASE_DIR, 'deployment', '.env'))

DOMAIN = os.getenv('DOMAIN')

CSRF_COOKIE_SECURE = bool(os.getenv('CSRF_COOKIE_SECURE'))
CSRF_COOKIE_HTTPONLY = bool(os.getenv('CSRF_COOKIE_HTTPONLY'))
CSRF_COOKIE_SAMESITE = os.getenv('CSRF_COOKIE_SAMESITE')

SESSION_COOKIE_AGE = int(os.getenv('SESSION_COOKIE_AGE'))
SESSION_COOKIE_SECURE = bool(os.getenv('SESSION_COOKIE_SECURE'))
SESSION_COOKIE_HTTPONLY = bool(os.getenv('SESSION_COOKIE_HTTPONLY'))
SESSION_COOKIE_SAMESITE = os.getenv('SESSION_COOKIE_SAMESITE')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('HOST'),
        'PORT': os.getenv('PORT_DB'),
    }
}
