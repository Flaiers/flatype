import os
import hashlib


def GenerateRandomHash(Model=None) -> str:
    hash = hashlib.md5(os.urandom(64)).hexdigest()

    if Model is not None:
        hash_exist = Model.objects.filter(owner_hash=hash)

        while hash_exist:
            hash = hashlib.md5(os.urandom(64)).hexdigest()
            hash_exist = Model.objects.filter(owner_hash=hash)
            continue

    return hash


def GenerateDataHash(data=None, Model=None) -> str:
    hash = hashlib.sha256(data).hexdigest()

    if Model is not None:
        hash_exist = Model.objects.filter(hash=hash)

    hash = str(hash_exist.first()).encode() if hash_exist else hash

    return hash
