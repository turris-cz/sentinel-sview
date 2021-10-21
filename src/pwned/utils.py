from enum import Enum
import json
import re
from jsonschema import validate, ValidationError

from logging import Logger

log = Logger(__name__)

_SOURCES_RE = re.compile(
    r"telnet|smtp|ftp|http|haas"
)  # split sources "{ftp,http}" etc.

# we need to map envvars to key names that are suitable for psycopg2 connection method
_ARG_MAP = {
    "POSTGRES_HOSTNAME": "host",
    "POSTGRES_DB": "database",
    "POSTGRES_USER": "user",
    "POSTGRES_PASSWORD": "password",
}


def _load_schema(msg_type):  # load json schema for validation
    """Helper function to load query schema"""
    rv = {}
    with open(f"schema/{msg_type}.json", "r") as f:
        rv = json.load(f)
    return rv


class Status(str, Enum):
    """Enumerator to make better control of the response status"""

    success = "SUCCESS"
    no_query = "NO_QUERY"
    validation_err = "VALIDATION_ERROR"


def compose_message(status, data=None, error=None, status_code=200):
    """Compose response message
    :status: status of the result action, enumerator _STATUS
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
        validate(response_load, _load_schema("response"))
    except ValidationError as e:
        log.warning(f"message {response_load} failed to validate, Error:{e}")
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


def filter_dictionary(source: dict, startstring: str):
    """Filter dictionary, or any object that have items method"""
    return {k: v for k, v in source.items() if k.startswith(startstring)}


def conform_arguments(dict, _map=_ARG_MAP):
    """By default conform pg arguments. Else remap keys based on provided ``_map``"""
    return {_map[k]: v for k, v in dict.items() if k in _map.keys()}


def unfold_pg_array(sources: str) -> list:
    """Unfold string that is result of pg.ARRAY `'{value,value,value}'` to list"""
    return _SOURCES_RE.findall(sources)
