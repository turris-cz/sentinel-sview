import csv
import psycopg2 as pg
from typing import Tuple

from utils import hash_it

from pwned import app
from pwned.utils import filter_dictionary, conform_arguments

# watch the special treatment of pg.ARRAY
_INSERT_STATEMENT = (
    "INSERT INTO passwords (count, password_hash, password_source) "
    "values (%s, %s, %s::data_source[]);"
)

# reference to pwned.__init__ settings
DB_SETTINGS = filter_dictionary(app.config, "POSTGRES")  # DB_CONN settings


def _parse_sources(ls: list) -> str:
    """Returns string of list encapsulated in {}
    helper function to conform data to what pg.ARRAY expects"""
    return f'{{{",".join(ls)}}}'


def _insert(cur, *args) -> int:
    """Inserts to database
    :cur: connetion cursor
    :args: row data"""
    return cur.execute(_INSERT_STATEMENT, (args))


def reset_passwords_table() -> None:
    con = pg.connect(**conform_arguments(DB_SETTINGS))
    cur = con.cursor()
    cur.execute("DELETE FROM passwords;")
    cur.execute("ALTER SEQUENCE passwords_id_seq RESTART;")
    with open("data/passwords.csv") as f:
        reader = csv.reader(f)
        _ = next(reader)  # skip the header
        for row in reader:
            count, password, sources_str = row
            sources = f'{{{sources_str}}}'
            _, _hash = hash_it(password)
            _insert(cur, count, _hash, sources)
    con.commit()



def insert_password(
    count: int, password: str, sources: list, override_hash=False
) -> Tuple[str, str]:
    """Helper function to insert data in database."""
    if override_hash:  # we need to 'hardcode' hash on some occasions
        _hash = password
        _stub = password[:6]
    else:  # sometimes we don't
        _stub, _hash = hash_it(password)
    _sources = _parse_sources(sources)

    con = pg.connect(**conform_arguments(DB_SETTINGS))
    with con.cursor() as cur:
        _insert(cur, count, _hash, _sources)
    con.commit()
    con.close()
    return _stub, _hash
