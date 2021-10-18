from flask import Flask, request
from .database import load_dev, load_production

from .backend import proc_leaked
from .config import DevelopmentConfig, ProductionConfig, TestingConfig

app = Flask(__name__)
if app.config['ENV'] == 'development':
    app.config.from_object(DevelopmentConfig)
    db_settings = {key:value for key, value in app.config.items() if key.startswith("DB")}
    load_dev(**db_settings)

elif app.config['ENV'] == 'testing':
    app.config.from_object(TestingConfig)
else:
    app.config.from_object(ProductionConfig)
    load_production()


@app.route("/api/leaked/", methods=["POST"])
def leaked_advanced():
    """Route for selecting passwords from advanced database"""
    return proc_leaked(**request.json)

