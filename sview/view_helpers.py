import hashlib


def get_tokens_hash(device_tokens):
    if not device_tokens:  # Both empty or None
        return None

    tokens_string = "".join(device_tokens).replace("'", '"')
    hash_object = hashlib.sha256()
    hash_object.update(tokens_string.encode("utf-8"))

    return hash_object.hexdigest()[0:10]
