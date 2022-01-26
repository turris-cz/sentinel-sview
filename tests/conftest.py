from distutils.command.clean import clean
import logging
import pytest
from sview import create_app

from utils import hash_it
from utils.pg_manager import insert_password, cleanup


@pytest.fixture
def extra_passwords(request):
    """insert extra password with the same start hash as first item to test
    whether it is posissible to return more records using API"""

    items = request.param
    first_password = items.pop(0)

    ids = [first_password[0]]  # save ids to cleanthem up later

    stub, first_hash = insert_password(*first_password)

    hashes = [first_hash]  # save the hash for later check

    for idn, password, count, sources in items:
        ids.append(idn)
        _, _hash = hash_it(password)
        # switch first 6 characters to be the same as for `ruris`
        _hash = stub + _hash[6:]
        insert_password(idn, _hash, count, sources, override_hash=True)
        hashes.append(_hash)
    yield stub, hashes

    cleanup(tuple(ids))


@pytest.fixture
def client():
    """Basic client fixture"""
    app = create_app()
    with app.test_client() as client:
        with app.app_context() as ctx:
            yield client


@pytest.fixture
def bad_hash(client, request):

    idn, _hash, count, sources = request.param
    insert_password(idn, _hash, count, sources, override_hash=True)
    yield

    cleanup((idn,))
