import uuid, base64


def GenerateHash(Model=None):
    hash = base64.urlsafe_b64encode(uuid.uuid1().bytes)[:32]

    if Model is not None:
        hash_exist = Model.objects.filter(owner_hash=hash)

        while hash_exist:
            hash = base64.urlsafe_b64encode(uuid.uuid1().bytes)[:32]
            hash_exist = Model.objects.filter(owner_hash=hash)
            continue

    hash = hash.decode('utf-8')

    return hash
