import pytest
from passy.database.models import Password

from utils import hash_it, message_it


def test_unsafe_password(client):
    """Test if sent hash corresponds to some we have"""

    def _f(x):
        return x["hash"] == full_hash

    pword = "hikvision"
    stub, full_hash = hash_it(pword)
    res = client.post("/api/leaked/", json=message_it(stub))
    assert res.json["status"] == "SUCCESS"
    data = res.json["data"]
    result = list(filter(_f, data))
    assert len(result) == 1
    assert result[0]["hash"] == full_hash


def test_safe_password(client):
    """Test if sent hash does not correspond to any"""

    def _f(x):
        return x["hash"] == full_hash

    pword = "safe"
    stub, full_hash = hash_it(pword)
    res = client.post("/api/leaked/", json=message_it(stub))
    assert res.json["status"] == "NO_QUERY"
