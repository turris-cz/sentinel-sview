from hashlib import sha1
from utils import hash_it

from passy import app
import psycopg2 as pg

_INSERT_STMNT = "INSERT INTO passwords (count, password_hash, password_source) " \
"values (%s, %s, %s::data_source[]);"


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


def insert_password(password: str, count: int, sources: list):
    """Helper function to insert data in database."""
    _hash, _ =  hash_it(password)
    con  = pg.connect
    with con.cursor() as cur:
        for pword in g:
            _hash = _hash_it(pword)
            _sources = sample(_TYPE, randint(1,5))
            _count = randint(1,250)
            print(_insert(cur, _count,_hash,_sources))
        cur.commit()

    con.close()