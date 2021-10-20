import pytest

from passy.database.models import Password
from pg_manager import insert_password
from utils import hash_it


def test_testing_data_count(client):
    """Test if `testing_data.sql` got reset correctly to default state."""
    d = Password.select().count()
    assert d == 115


def test_database(client):
    """Test inserting to database for testing purposes."""
    stub, _ = insert_password(50, "ruris", ["smtp", "haas"])
    t = Password.select().where(Password.password_hash.startswith(stub)).get()
    assert t.count == 50  # do not confuse with model `count()` method


@pytest.mark.parametrize('extra_passwords', [
    [
        (50, "ruris", ["smtp", "haas"]),
    (50, 'morris', ["ftp", "http", "smtp"]),
    (100, 'rorys',["haas", "telnet"]),
    (45, 'dennis', ["smtp","ftp"])
    ]
    ],indirect=True
)
def test_extra_passwords_fixture(client, extra_passwords):
    """We would like to test the fixture"""
    stub, db_hashes =  extra_passwords  # fixture generates list of inserted hashes
    t = Password.select(
        Password.password_hash
    ).where(
        Password.password_hash.startswith(stub)
    )

    assert t.count() == 4  # selected password count is correct
    # convert query result to list
    selected_hashes = [i.password_hash for i in t.iterator()]

    # and hopefully wha have correct result here
    assert db_hashes == selected_hashes 
