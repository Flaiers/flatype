import os

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DOMAIN = os.getenv('DOMAIN')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('POSTGRES_DB'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('HOST'),
        'PORT': 5432,
    }
}
