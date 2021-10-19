from re import I
from flask import Flask, request
from .database import load_dev, load_postgres

from .backend import proc_leaked

import os

app = Flask(__name__)

try:
    from .config import DevelopmentConfig, ProductionConfig
except ImportError as e:
    if app.config['ENV'] == "testing":
        pass
    else:
        raise ImportError(f'You need to setup `config.py` to be able to run this app. Error:{e}' ) from e 


if app.config['ENV'] == 'development':
    app.config.from_object(DevelopmentConfig)
    db_settings = {key:value for key, value in app.config.items() if key.startswith("DB")}
    load_dev(**db_settings)

elif app.config['ENV'] == 'testing':
    app.config['DB_NAME'] = os.getenv('POSTGRES_DB')
    app.config['DB_USERNAME'] = os.getenv('POSTGRES_USER')
    app.config['DB_PASSWORD'] = os.getenv('POSTGRES_PASSWORD')
    app.config['DB_HOSTNAME'] = "postgres"
    load_postgres()
else:
    app.config.from_object(ProductionConfig)
    load_postgres()


@app.route("/api/leaked/", methods=["POST"])
def leaked_advanced():
    """Route for selecting passwords from advanced database"""
    return proc_leaked(**request.json)
