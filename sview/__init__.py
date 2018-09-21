from logging.config import dictConfig

from flask import Flask


def setup_logging():
    dictConfig({
        "version": 1,
        "root": {
            "level": "INFO",
        },
    })


def create_app(additional_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object("sview.default_settings")
    app.config.from_pyfile("local.cfg", silent=True)
    app.config.from_envvar("FLASK_APP_SETTINGS", silent=True)
    if additional_config:
        app.config.from_mapping(additional_config)

    setup_logging()

    from .data import databp
    app.register_blueprint(databp)

    from .filters import register_filters
    register_filters(app)

    return app
