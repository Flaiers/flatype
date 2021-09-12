import os
import hashlib


def GenerateRandomHash(model=None) -> str:
    hash = hashlib.sha256(os.urandom(64)).hexdigest()

    if model is not None:
        hash_exist = model.objects.filter(owner_hash=hash)

        while hash_exist:
            hash = hashlib.sha256(os.urandom(64)).hexdigest()
            hash_exist = model.objects.filter(owner_hash=hash)
            continue

    return hash


def GenerateDataHash(data=None, model=None) -> str:
    hash = hashlib.sha256(data).hexdigest()

    if model is not None:
        hash_exist = model.objects.filter(hash=hash)

    hash = str(hash_exist.first()).encode() if hash_exist else hash

    return hash
