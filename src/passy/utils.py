from jsonschema import validate
import json
from hashlib import sha256
from .database.models import Password

hash_it = lambda pwd: sha256(pwd.encode()).hexdigest()


def check_sha256(request_stub):  # hash stub sent from frontend
    """Check requested stub against database"""
    resuln = []
    passwords = Password.select()
    for entry in passwords.iterator():
        hexdg = sha256(entry.password.encode()).hexdigest()
        if hexdg[: len(request_stub)] == request_stub:
            resuln.append({"hash": hexdg, "count": entry.count})
    return resuln


def load_schema():
    """Helper function to load query schema"""
    rv = {}
    with open("schema/passy.json", "r") as f:
        rv = json.load(f)
    return rv
