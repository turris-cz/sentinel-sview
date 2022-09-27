from .utils import validate_decor, compose_message, Status, deserialize
from typing import Tuple

from sview.extensions import db


def get_hash(stub) -> Tuple[dict, int]:
    data = []
    params = {"hs": f"{stub}%"}
    res = db.session.execute(_SELECT, params=params)
    if res.rowcount < 1:
        return compose_message(Status.no_query)
    else:
        for item in map(deserialize, res):
            data.append(item)
        return compose_message(Status.success, data)


_SELECT = """SELECT password_hash, password_count, password_source FROM passwords_pwned
    WHERE password_hash LIKE :hs;
"""


@validate_decor
def process_request(**json_data) -> Tuple[dict, int]:
    """Processing request from client."""
    stub = json_data["hash"]
    return get_hash(stub=stub)
