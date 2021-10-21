import pytest
from pwned.database.models import Password
from functools import partial

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


def filter_on_count(val, data):
    return list(filter(partial(_fltr, "count", val), data))[0]


def _fltr(on, val, item):
    return item[on] == val


def test_safe_password(client):
    """Test if sent hash does not correspond to niether one in database"""

    def _f(x):
        return x["hash"] == full_hash

    pword = "safe"
    stub, full_hash = hash_it(pword)
    res = client.post("/api/leaked/", json=message_it(stub))
    assert res.json["status"] == "NO_QUERY"


@pytest.mark.parametrize(
    "extra_passwords",
    [
        [
            (1, "morris", ["ftp", "http", "smtp"]),
            (25, "korys", ["haas", "telnet"]),
            (30, "sumys", ["smtp", "ftp"]),
            (50, "dennis", ["smtp", "haas"]),
        ]
    ],
    indirect=True,
)
def test_multiple_passwords_common_hash(client, extra_passwords):
    """Test if api returns all hashes that start with provided hash"""
    _, db_hashes = extra_passwords
    pword = "morris"
    stub, _ = hash_it(pword)
    res = client.post("/api/leaked/", json=message_it(stub))
    assert res.json["status"] == "SUCCESS"
    data = res.json["data"]
    received_hashes = [i["hash"] for i in data]
    assert set(db_hashes) == set(received_hashes)

    # we did not save the hashes, but we know the counts
    # of passwords usage

    morris = filter_on_count(1, data)
    korys = filter_on_count(25, data)
    sumys = filter_on_count(30, data)
    dennis = filter_on_count(50, data)

    assert morris["sources"] == ["ftp", "http", "smtp"]
    assert korys["sources"] == ["haas", "telnet"]
    assert sumys["sources"] == ["smtp", "ftp"]
    assert dennis["sources"] == ["smtp", "haas"]


def test_validation_on_request(client):
    """Test message sent by client"""
    stub, _ = hash_it("secret")
    stub = stub[:-1]
    res = client.post("/api/leaked/", json=message_it(stub))
    assert res.json["status"] == "VALIDATION_ERROR"
    error = res.json["error"]
    assert "does not match '^[a-z0-9]{6}$'" in error
