from flask import current_app, g

from werkzeug.local import LocalProxy

import sqlite3
import types


def namespace_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return types.SimpleNamespace(d)


def get_db():
    db = getattr(g, '_database', None)

    if db is None:
        db = g._database = sqlite3.connect(current_app.config["DB_PATH"])
        db.isolation_level = None
        db.row_factory = namespace_factory

    return db


db = LocalProxy(get_db)
