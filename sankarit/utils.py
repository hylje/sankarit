# -*- coding: utf-8 -*-
# Utility functions and hooks

import psycopg2

import functools

from flask import g, session, redirect, flash

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

def login_required(controller):
    @functools.wraps(controller)
    def wrapper(*args, **kwargs):
        if session.get("playerid") is None:
            flash(u"Tämä sivu vaatii kirjautumisen. Kirjaudu ja yritä uudelleen.", "error")
            return redirect("login")
        else:
            return controller(*args, **kwargs)

    return wrapper
