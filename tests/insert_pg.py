from hashlib import sha1
from utils import hash_it

from passy import app
import psycopg2 as pg

from passy.utils import filter_dictionary, conform_arguments


_INSERT_STMNT = "INSERT INTO passwords (count, password_hash, password_source) " \
"values (%s, %s, %s::data_source[]);"

_DB_SETTINGS = filter_dictionary(app.config, "POSTGRES")


def _parse_sources(ls: list) -> str:
    """Returns string of list encapsulated in {}"""
    return f'{{{",".join(ls)}}}'


def _insert(cur, *args):
    """ Inserts to database
    :cur: connetion cursor
    :args: row data"""
    return cur.execute(
        _INSERT_STMNT,
        (args)
    )


def insert_password(password: str, count: int, sources: list) -> str:
    """Helper function to insert data in database."""
    _stub, _hash =  hash_it(password)
    _sources = _parse_sources(sources)

    con  = pg.connect(**conform_arguments(_DB_SETTINGS))
    with con.cursor() as cur:
        _insert(cur, count, _hash,_sources)
    con.commit()
    con.close()
    return _stub
