from flask import Flask, request
from pwned.utils import filter_dictionary
from .database import load_postgres

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
    """Route for selecting passwords from advanced database"""
    return proc_leaked(**request.json)
