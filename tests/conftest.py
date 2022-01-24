import pytest
import os

from sview import create_app
from utils import hash_it
from pg_manager import reset_passwords_table, insert_password
from pwned_backend.utils import filter_dictionary


# TODO: Iterativly redo the tests, sql does not work

@pytest.fixture
def extra_passwords(client, request):
    """insert extra password with the same start hash as first item"""
    items = request.param
    first_password = items.pop(0)

    stub, first_hash = insert_password(*first_password)

    hashes = [first_hash]  # save the hash for later check

    for count, password, sources in items:
        _, _hash = hash_it(password)
        # switch first 6 characters to be the same as for `ruris`
        _hash = stub + _hash[6:]
        insert_password(count, _hash, sources, override_hash=True)
        hashes.append(_hash)
    return stub, hashes


@pytest.fixture
def client():
    reset_passwords_table()
    """Flask client fixture."""
    
    pg_settings = filter_dictionary(os.environ, "POSTGRES")
    pg_settings.update({"FLASK_ENV": os.environ.get["FLASK_ENV"]})

    app = create_app(**pg_settings)
    with app.test_client() as client:
        yield client
