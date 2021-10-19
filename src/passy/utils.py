from jsonschema import validate
import json

from jsonschema import validate, ValidationError


def _load_schema():  # load json schema for validation
    """Helper function to load query schema"""
    rv = {}
    with open("schema/passy.json", "r") as f:
        rv = json.load(f)
    return rv


_SCHEMA = _load_schema()

_STATUS = {1: "SUCCESS", 2: "NO_QUERY", 3: "VALIDATION_ERROR"}

_ARG_MAP = {
    "POSTGRES_HOSTNAME": "host",
    "POSTGRES_DB" : "database",
    "POSTGRES_USER": "user",
    "POSTGRES_PASSWORD": "password"
}

def compose_message(status, data=None, error=None, status_code=200):
    """Do not confuse `status` with response code, always returning `200`
    :retval: tuple with load and response code"""
    response_load = {
        "msg_type": "response",
        "status": _STATUS[status],
    }
    if data:
        response_load.update({"data": data})
    if error:
        response_load.update({"error": error})
    # validate outgoing log error to logger
    return response_load, 200


def validate_decor(func):
    def wrapper(**json_data):
        try:
            validate(json_data, _SCHEMA)
            return func(**json_data)
        except ValidationError as e:
            return compose_message(3, error=e, status_code=400)

    return wrapper


def filter_dictionary(source: dict, startstring: str):
   return  {k: v for k, v in source.items() if k.startswith(startstring)}


def conform_arguments(dict, _map=_ARG_MAP):
    """By default conform pg arguments."""
    return {_map[k]:v for k, v in dict.items()}
