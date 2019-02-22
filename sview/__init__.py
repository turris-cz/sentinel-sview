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

    from .dashboard import dashboard
    from .opendata import opendata
    from .passwords import passwords
    from .attackers import attackers
    app.register_blueprint(dashboard)
    app.register_blueprint(opendata, url_prefix="/opendata")
    app.register_blueprint(passwords, url_prefix="/passwords")
    app.register_blueprint(attackers, url_prefix="/attackers")

    from .extensions import babel
    from .extensions import cache
    from .extensions import mail
    from .extensions import db
    from .extensions import migrate
    from .extensions import redis
    from .extensions import rq

    babel.init_app(app)
    cache.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    redis.init_app(app)
    rq.init_app(app)

    from .filters import register_filters
    register_filters(app)

    from .cli import register_cli_commands
    from .cli import register_shell_context
    register_cli_commands(app)
    register_shell_context(app)

    return app
