from flask import Flask, request, jsonify
from pwned.utils import filter_dictionary
from .database import load_postgres

_HEADERS = {
    'Content-Type': 'application/json; charset=utf-8'
}

from logging import Logger

_logger = Logger(__name__)

import json

from .backend import proc_leaked

import os

app = Flask(__name__)

try:
    from .config import DevelopmentConfig, ProductionConfig
except ImportError as e:
    if app.config["ENV"] == "testing":
        pass
    else:
        raise ImportError(
            f"You need to setup `config.py` to be able to run this app. Error:{e}"
        ) from e

if app.config["ENV"] == "development":
    app.config.from_object(DevelopmentConfig)

elif app.config["ENV"] == "testing":
    pg_settings = filter_dictionary(os.environ, "POSTGRES")
    app.config.from_mapping(pg_settings)
    app.config["POSTGRES_HOSTNAME"] = "postgres"
else:
    app.config.from_object(ProductionConfig)

db_settings = filter_dictionary(app.config, "POSTGRES")
load_postgres(**db_settings)


@app.route("/api/leaked/", methods=["POST"])
def leaked_advanced():
    """Route for selecting passwords from database"""
    if not request.json:
        args = json.loads(request.get_data())
    else:
        args = request.json
    try:
        data, code = proc_leaked(**args)
        return data, code, _HEADERS
    except Exception as e:
        _logger.error(f'Error: {e}.')
