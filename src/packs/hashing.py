import os
import hashlib


def GenerateRandomHash() -> str:
    hash = hashlib.sha256(os.urandom(64)).hexdigest()

    return hash


def GenerateDataHash(data=None, model=None) -> str:
    hash = hashlib.sha256(data).hexdigest()

    if model is not None:
        hash_exist = model.objects.filter(hash=hash)

    hash = str(hash_exist.first()).encode() if hash_exist else hash

    return hash
