from hashlib import sha1
from utils import hash_it

from passy import app
import psycopg2 as pg

from passy.utils import filter_dictionary, conform_arguments


# watch the special treatment of pg.ARRAY
_INSERT_STMNT = (
    "INSERT INTO passwords (count, password_hash, password_source) "
    "values (%s, %s, %s::data_source[]);"
)

# reference to passy.__init__ settings
_DB_SETTINGS = filter_dictionary(app.config, "POSTGRES")  # DB_CONN settings


def _parse_sources(ls: list) -> str:
    """Returns string of list encapsulated in {}
    helper function to conform data to what pg.ARRAY expects"""
    return f'{{{",".join(ls)}}}'


def _insert(cur, *args):
    """Inserts to database
    :cur: connetion cursor
    :args: row data"""
    return cur.execute(_INSERT_STMNT, (args))


def insert_password(
    password: str, count: int, sources: list, override_hash=False
) -> str:
    """Helper function to insert data in database."""
    if override_hash:  # we need to 'hardcode' hash on some occasions
        _hash = password
        _stub = password[:6]
    else:  # sometimes we don't
        _stub, _hash = hash_it(password)
    _sources = _parse_sources(sources)

    con = pg.connect(**conform_arguments(_DB_SETTINGS))
    with con.cursor() as cur:
        _insert(cur, count, _hash, _sources)
    con.commit()
    con.close()
    return _stub
