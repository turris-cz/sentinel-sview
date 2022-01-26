from .utils import validate_decor, compose_message, Status


from sview.extensions import db


def deserialize(row):
    """Deserialize selected row"""
    return {
        "hash": row.password_hash,
        "count": row.count,
        "sources": row.password_source.strip("{").strip("}").split(",")
    }

_SELECT = """SELECT * FROM passwords_pwned
    WHERE password_hash LIKE :hs;
"""


@validate_decor
def proc_leaked(**json_data):
    """Processing request from client."""
    stub = json_data["hash"]
    data = []
    params = {"hs":f"{stub}%"}
    res = db.session.execute(_SELECT, params=params)
    if res.rowcount < 1:
        return compose_message(Status.no_query)
    else:
        for item in map(deserialize,res):
            data.append(item)
        return compose_message(Status.success, data)
