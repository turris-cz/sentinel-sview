import pytest

from os import path

from passy import app
from passy.database import create_testing, load_dev


@pytest.fixture
def client():
    """Flask client fixture."""
    p = path.dirname(path.realpath(__file__))
    create_testing(p + "/files/testing_data.sql")

    with app.test_client() as client:
        yield client
