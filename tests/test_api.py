import pytest

_ENDPOINT = "/passcheck/apiv1/"

_MOCK = "e5e9fa1ba31ecd1ae84f75caaa474f3a663f05f4"


def message_it(_hash):
    return {"msg_type": "request", "hash": _hash}


def test_long_hash(client):
    res = client.post(_ENDPOINT, json=message_it(_MOCK))
    assert res.json["status"] == "VALIDATION_ERROR"


@pytest.mark.parametrize(
    "mock_db_call",
    [
        [
            {
                "hash": "e5e9fa1ba31ecd1ae84f75caaa474f3a663f05f4",
                "count": 2,
                "sources": ["smtp"],
            }
        ]
    ],
    indirect=True,
)
def test_record_exists(client, mock_db_call):
    res = client.post(_ENDPOINT, json=message_it(_MOCK[:6]))
    assert res.status_code == 200
    load = res.json
    assert set(load.keys()) == {"msg_type", "status", "data"}
    assert load["msg_type"] == "response"
    assert load["status"] == "SUCCESS"
    assert load["data"][0]["hash"] == "e5e9fa1ba31ecd1ae84f75caaa474f3a663f05f4"


@pytest.mark.parametrize("mock_db_call", [None], indirect=True)
def test_does_not_exist(client, mock_db_call):
    res = client.post(_ENDPOINT, json=message_it(_MOCK[:6]))
    assert res.status_code == 200
    load = res.json
    assert set(load.keys()) == {"msg_type", "status"}
    assert load["msg_type"] == "response"
    assert load["status"] == "NO_QUERY"
