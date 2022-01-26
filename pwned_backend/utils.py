from enum import Enum
from http.client import TEMPORARY_REDIRECT

import json
from jsonschema import validate, ValidationError

import logging


def _load_schema(msg_type):  # load json schema for validation
    """Helper function to load given `msg_type` schema"""
    rv = {}
    with open(f"schema/{msg_type}.json", "r") as f:
        rv = json.load(f)
    return rv


class Status(str, Enum):
    """Enumerator to define the response status"""

    success = "SUCCESS"
    no_query = "NO_QUERY"
    validation_err = "VALIDATION_ERROR"


def compose_message(status, data=None, error=None, status_code=200):
    """Compose response message
    :status: status of the result action, enumerator Status
    :retval: tuple with load and response code"""
    response_load = {
        "msg_type": "response",
        "status": status,
    }
    if data:
        response_load.update({"data": data})
    if error:
        response_load.update({"error": error})
    try:
        schema = _load_schema("response")
        validate(response_load, schema)
    except ValidationError as e:
        logging.warning(
            f"Validation error for outgoing message {response_load}; failed validation against schema {schema}, Error:{e}"
        )
    return response_load, status_code


def validate_decor(func):
    """Schema validation decorator"""

    def wrapper(**json_data):
        try:
            validate(json_data, _load_schema("request"))
            return func(**json_data)
        except ValidationError as e:
            return compose_message(Status.validation_err, error=f"{e}", status_code=400)

    return wrapper
