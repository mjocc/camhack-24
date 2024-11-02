# code modified from https://flask.palletsprojects.com/en/stable/tutorial/database/

import sqlite3
from datetime import datetime

from flask import g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("db.sqlite3", detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


sqlite3.register_converter("timestamp", lambda v: datetime.fromisoformat(v.decode()))
