import logging
from os import error
from jsonschema import validate, ValidationError

from .database.models import PasswordWithHash
from .utils import hash_it, check_sha256, load_schema

_LOGGER = logging.getLogger(__name__)
_SCHEMA = load_schema()

_STATUS = {
    1: "SUCCESS",
    2: "NO_QUERY",
    3: "VALIDATION_ERROR"
}

def _validate(func):
    def wrapper(**json_data):
        try:
            validate(json_data, _SCHEMA)
            return func(**json_data)
        except ValidationError as e:
            return compose_message(3, error=e, status_code=400)
    return wrapper


def compose_message(status, data=None, error=None, status_code=200):
    """Do not confuse `status` with response code, always returning `200`
    :retval: tuple with load and response code"""
    response_load = {
        "msg_type": "response",
        "status":_STATUS[status],
    }
    if data:
        response_load.update({"data":data})
    if error:
        response_load.update({"error": error})
    # validate outgoing log error to logger
    return response_load, 200


@_validate
def proc_leaked(**json_data):
    """Processing request from client"""
    stub = json_data["hash"]
    result = check_sha256(stub)
    if len(result) < 1:
        return compose_message(2)
    else:
        return compose_message(1, result)

@_validate
def proc_leaked_advanced(**json_data):
    """Processing request from client"""
    stub = json_data["hash"]
    data = []
    sel = PasswordWithHash.select().where(PasswordWithHash._hash==stub)
    if sel.count() < 1:
        return compose_message(2)
    else:
        for item in sel.iterator():  # pewee select object provides nice `iterator()` method
            data.append({"hash":hash_it(item.password), "count": item.count})
        return compose_message(1, data)
