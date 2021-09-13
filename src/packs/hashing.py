import os
import hashlib

from django.conf import settings
from django.utils.crypto import salted_hmac


def generate_random_hash() -> str:
    hash = hashlib.sha256(os.urandom(64)).hexdigest()

    return hash


def generate_data_hash(salt=None, data=None, model=None) -> str:
    if salt is None:
        salt = 'django.packs.hashing.generate_data_hash'
    hash = salted_hmac(salt, data, algorithm=settings.DEFAULT_HASHING_ALGORITHM).hexdigest()

    if model is not None:
        hash_exist = model.objects.filter(hash=hash)

    hash = str(hash_exist.first()).encode() if hash_exist else hash

    return hash
