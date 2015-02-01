import os

from flask import Flask


app = Flask("sankarit")
app.config.update(
    PG_USERNAME=None,
    PG_PASSWORD=None,
    PG_DATABASE="sankarit",
    DEBUG=True
)

if "SANKARIT_SETTINGS_FILE" in os.environ:
    app.config.from_envvar("SANKARIT_SETTINGS_FILE")

# import controllers and hooks to set them up
import sankarit.controllers
import sankarit.utils
