from dotenv import load_dotenv

from pathlib import Path

import os

BASE_DIR = Path(__file__).parent.parent.parent.parent

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
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('HOST'),
    }
}
