import pytest
from sview import create_app

from unittest.mock import patch

from unittest.mock import patch
from password_checker.utils import compose_message as _cm, Status


@pytest.fixture
def client():
    """Basic client fixture"""
    app = create_app()
    with app.test_client() as client:
        with app.app_context() as ctx:
            yield client


@pytest.fixture
def mock_db_call(request):
    if request.param is None:
        retval = _cm(Status.no_query)
    else:
        retval = _cm(Status.success, request.param)
    with patch("password_checker.get_hash", return_value=retval) as m:
        yield m
