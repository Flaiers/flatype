from django.utils.crypto import salted_hmac

from django.conf import settings

import hashlib
import os


def generate_random_hash() -> str:
    return hashlib.sha256(os.urandom(64)).hexdigest()


def generate_data_hash(salt=None, data=None, model=None) -> str:
    if salt is None:
        salt = 'django.packs.hashing.generate_data_hash'
    hash = salted_hmac(salt, data, algorithm=settings.DEFAULT_HASHING_ALGORITHM).hexdigest()

    if model is not None:
        exist_hash = model.objects.filter(hash=hash).first()

    return exist_hash if exist_hash else hash
