# Utility functions and hooks

import psycopg2

from flask import g
from sankarit import app

@app.before_request
def before_request():
    g.db = get_connection()

@app.teardown_request
def teardown_request(exc):
    db = getattr(g, "db", None)
    if db is not None:
        db.close()

def get_connection():
    return psycopg2.connect(
        username=app.config["PG_USERNAME"],
        password=app.config["PG_PASSWORD"],
        database=app.config["PG_DATABASE"]
    )
