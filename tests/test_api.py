import pytest
from passy.database.models import Password

from utils import hash_it, message_it


def test_password_unsafe(client):
    """Test if password hash in database"""

    def _f(x):
        return x["hash"] == full_hash

    pword = "secret"
    stub, full_hash = hash_it(pword)
    res = client.post("/api/leaked/", json=message_it(stub))
    assert res.json["status"] == "SUCCESS"
    data = res.json["data"]
    result = list(filter(_f, data))
    assert len(result) == 1
    assert result[0]["hash"] == full_hash


def test_password_safe(client):
    """User sent 6 chars of hash of password that is not in database."""
    pword = "zabka"
    stub, full_hash = hash_it(pword)
    res = client.post("/api/leaked/", json=message_it(stub))
    assert res.json["status"] == "NO_QUERY"


def test_with_advanced_database_unsafe(client):
    """Test if sent hash corresponds to some we have"""

    def _f(x):
        return x["hash"] == full_hash

    pword = "abAuXwyvR"
    stub, full_hash = hash_it(pword)
    res = client.post("/api/leaked_advanced/", json=message_it(stub))
    assert res.json["status"] == "SUCCESS"
    data = res.json["data"]
    result = list(filter(_f, data))
    assert len(result) == 1
    assert result[0]["hash"] == full_hash


def test_with_advanced_database_safe(client):
    """Test if sent hash corresponds to some we have"""

    def _f(x):
        return x["hash"] == full_hash

    pword = "safe"
    stub, full_hash = hash_it(pword)
    res = client.post("/api/leaked_advanced/", json=message_it(stub))
    assert res.json["status"] == "NO_QUERY"
