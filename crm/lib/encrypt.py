import hashlib


def hmac_sha256(string):
    s = string.encode('utf8')
    hash_ = hashlib.sha256(s).hexdigest()
    return hash_
