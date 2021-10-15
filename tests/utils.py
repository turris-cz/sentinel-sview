from hashlib import sha256


def hash_it(string, k=6):
    """Retruns `k` long slice and hash."""
    hashed = sha256(string.encode()).hexdigest()
    return hashed[:k], hashed


def message_it(_hash):
    return {"msg_type": "request", "hash": _hash}
