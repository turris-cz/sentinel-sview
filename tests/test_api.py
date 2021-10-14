import pytest
from base.models import Password


def test_password_safe(client):
    res = client.post('/api/leaked/', json={"password":"secret"})
    assert res.json['status'] == 'USED'


def test_password_unsafe(client):
    res = client.post('/api/leaked/', json={"password":"zabka"})
    assert res.json['status'] == 'SAFE'
