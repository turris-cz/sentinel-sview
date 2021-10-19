import pytest

from passy import app


@pytest.fixture
def client():
    """Flask client fixture."""
    with app.test_client() as client:
        yield client
