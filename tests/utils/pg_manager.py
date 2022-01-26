from typing import Tuple

from utils import hash_it


from sview.extensions import db

_INSERT_STATEMENT = (
    "INSERT INTO passwords_pwned (id, password_hash, count, password_source) "
    "values (%s, %s, %s, %s::data_source[]);"
)


def _parse_sources(ls: list) -> str:
    """Returns string of list encapsulated in {}
    helper function to conform data to what pg.ARRAY expects"""
    return f'{{{",".join(ls)}}}'


def _insert(cur, *args) -> int:
    """Inserts to database
    :cur: connetion cursor
    :args: row data"""
    return cur.execute(_INSERT_STATEMENT, (args))


def insert_password(
    idn: int, password: str, count: int, sources: list, override_hash=False
) -> Tuple[str, str]:
    """Helper function to insert data in database."""
    if override_hash:  # we need to 'hardcode' hash on some occasions
        _hash = password
        _stub = password[:6]
    else:  # sometimes we don't
        _stub, _hash = hash_it(password)
    _sources = _parse_sources(sources)

    con = db.engine.raw_connection()
    with con.cursor() as cur:
        _insert(cur, idn, _hash, count, _sources)
    con.commit()
    con.close()
    return _stub, _hash


def cleanup(ids: tuple):
    db.session.execute(
        """delete from passwords_pwned where id in :ids;""",
        {
            "ids": ids,
        },
    )
    db.session.commit()
