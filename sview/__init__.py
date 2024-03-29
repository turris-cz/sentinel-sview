from logging.config import dictConfig

from flask import Flask
from flask_breadcrumbs import Breadcrumbs


def setup_logging():
    dictConfig(
        {
            "version": 1,
            "root": {
                "level": "INFO",
            },
        }
    )


def create_app(additional_config=None):
    app = Flask(__name__, instance_relative_config=True)

    Breadcrumbs(app=app)

    from . import default_settings

    app.config.from_object(default_settings)
    app.config.from_pyfile("local.cfg", silent=True)
    app.config.from_envvar("FLASK_APP_SETTINGS", silent=True)
    if additional_config:
        app.config.from_mapping(additional_config)

    setup_logging()

    from .statistics import statistics
    from .opendata import opendata
    from .web import web
    from .dynfw import dynfw
    from .password_checker import pass_check
    from .report import report

    app.register_blueprint(statistics)
    app.register_blueprint(opendata, url_prefix="/opendata")
    app.register_blueprint(web)
    app.register_blueprint(dynfw)
    app.register_blueprint(pass_check, url_prefix="/passcheck")
    app.register_blueprint(report)

    from .extensions import babel
    from .extensions import cache
    from .extensions import mail
    from .extensions import db
    from .extensions import redis
    from .extensions import rq

    babel.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    redis.init_app(app)
    rq.init_app(app)

    from .filters import register_filters

    register_filters(app)

    from .cli import register_cli_commands

    register_cli_commands(app)

    return app
