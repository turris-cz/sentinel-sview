import pytest
from base.models import Password


def test_testing_data_count(client):
    """Test if `testing_data.sql` got loadded correctly to `:memory: database`"""
    d = Password.select().count()
    assert d == 1041


def test_database(client):
    """Test _inserting to_ and _selecting from_ `:memory:` database"""
    p = Password(password="ruris", count=50)
    p.save()

    t = Password.select().where(Password.password == "ruris").get()
    assert t.count == 50
    assert Password.select().count() == 1042
