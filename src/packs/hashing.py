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


def GenerateDataHash(Model=None, data=None) -> str:
    hash = hashlib.sha256(data).hexdigest()

    if Model is not None:
        hash_exist = Model.objects.filter(hash=hash)

        while hash_exist:
            hash = hashlib.sha256(data).hexdigest()
            hash_exist = Model.objects.filter(hash=hash)
            continue

    return hash
