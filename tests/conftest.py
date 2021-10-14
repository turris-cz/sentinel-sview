import pytest
from pathlib import Path
from os import path

from passy import app
from base import create_testing


@pytest.fixture
def client():
    p = path.dirname(path.realpath(__file__))
    app.config["DATABASE"] = create_testing(p + "/files/testing_data.sql")

    with app.test_client() as client:
        yield client
