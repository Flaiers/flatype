import os
import hashlib


def GenerateHash(Model=None) -> str:
    hash = hashlib.md5(os.urandom(64)).hexdigest()

    if str(Model) == "<class 'core.models.Article'>":
        hash_exist = Model.objects.filter(owner_hash=hash)

        while hash_exist:
            hash = hashlib.md5(os.urandom(64)).hexdigest()
            hash_exist = Model.objects.filter(owner_hash=hash)
            continue

    elif str(Model) == "<class 'core.models.Storage'>":
        hash_exist = Model.objects.filter(hash=hash)

        while hash_exist:
            hash = hashlib.md5(os.urandom(64)).hexdigest()
            hash_exist = Model.objects.filter(hash=hash)
            continue

    return hash
