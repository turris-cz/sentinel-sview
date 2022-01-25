from distutils.command.clean import clean
import pytest
from sview import create_app

from utils import hash_it
from tests.utils.pg_manager import insert_password, cleanup


@pytest.fixture
def extra_passwords(client, request):
    """insert extra password with the same start hash as first item"""
    items = request.param
    first_password = items.pop(0)

    stub, first_hash = insert_password(*first_password)

    hashes = [first_hash]  # save the hash for later check

    ids = []

    for idn, password, count, sources in items:
        ids.append(idn)
        _, _hash = hash_it(password)
        # switch first 6 characters to be the same as for `ruris`
        _hash = stub + _hash[6:]
        insert_password(idn, _hash, count, sources, override_hash=True)
        hashes.append(_hash)
    yield stub, hashes

    cleanup(tuple(ids))


# @pytest.fixture
# def client():
#     reset_passwords_table()
#     """Flask client fixture."""
    
#     pg_settings = filter_dictionary(os.environ, "POSTGRES")
#     pg_settings.update({"FLASK_ENV": os.environ.get["FLASK_ENV"]})

#     app = create_app(**pg_settings)
#     with app.test_client() as client:
#         yield client



@pytest.fixture
def client():
    additional_config = {
        "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:secret@localhost/sentinel"
    }
    app = create_app(additional_config=additional_config)
    with app.test_client() as client:
        with app.app_context() as ctx:
            yield client
