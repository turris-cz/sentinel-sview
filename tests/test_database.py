import pytest

from passy.database.models import Password
from insert_pg import insert_password


def test_testing_data_count(client):
    """Test if `testing_data.sql` got loaded correctly to `:memory: database`"""
    d = Password.select().count()
    assert d > 114


def test_database(client):
    """Test inserting to database"""
    stub = insert_password("ruris", 50, ["smtp", "haas"])
    t = Password.select().where(Password.password_hash.startswith(stub)).get()
    assert t.count == 50
