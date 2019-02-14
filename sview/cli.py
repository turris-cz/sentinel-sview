import click

from flask import current_app
from flask.cli import with_appcontext

from .extensions import db

@click.command()
@with_appcontext
def clear_cache():
    """Clear application cache"""

    from .extensions import cache

    click.echo("Cache type: {}".format(current_app.config["CACHE_TYPE"]))
    click.echo("Cache at: {}".format(current_app.config["CACHE_DIR"]))

    cache.clear()

    click.echo("Cache cleared")


def register_cli_commands(app):
    app.cli.add_command(clear_cache)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
        }
