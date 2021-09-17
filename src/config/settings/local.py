from .base import os, BASE_DIR

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DOMAIN = os.getenv('LOCAL_DOMAIN')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
