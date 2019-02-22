import click

from flask import current_app
from flask.cli import with_appcontext

from .jobs import load_data_from_template
from .queries import QUERIES

from .extensions import db, redis


@click.command()
@with_appcontext
def clear_cache():
    """Clear application cache"""

    from .extensions import cache

    click.echo("Cache type: {}".format(current_app.config["CACHE_TYPE"]))
    click.echo("Cache at: {}".format(current_app.config["CACHE_DIR"]))

    cache.clear()

    click.echo("Cache cleared")


@click.command()
@with_appcontext
def queue_queries():
    """Add all cached queries to the queue"""
    for k in QUERIES.keys():
        click.echo("Queuing: {}".format(k))
        load_data_from_template.queue(k)


@click.command()
@click.argument("name", nargs=-1, required=True)
@with_appcontext
def queue_query(name):
    """Add cached query to the queue"""
    for k in name:
        click.echo("Queuing: {}".format(k))
        load_data_from_template.queue(k)


@click.command()
@with_appcontext
def check_redis():
    """Check state of data in redis"""
    size = 0
    available = []
    missing = []

    for k in QUERIES.keys():
        data = redis.get(k)
        if data:
            available.append(k)
            size += len(data)
        else:
            missing.append(k)

    if available:
        click.echo("Stored keys:")
        for k in available:
            click.echo("  - {}".format(k))
    if missing:
        click.echo("Missing keys:")
        for k in missing:
            click.echo("  - {}".format(k))
    if available:
        click.echo("")
        click.echo("Keys occupy:  {}".format(_human_readable_bytes(size)))


def _human_readable_bytes(size):
    from math import log2
    _suffixes = ['bytes', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB']
    order = int(log2(size) / 10) if size else 0
    return '{:.4g} {}'.format(size / (1 << (order * 10)), _suffixes[order])


def register_cli_commands(app):
    app.cli.add_command(clear_cache)
    app.cli.add_command(queue_queries)
    app.cli.add_command(queue_query)
    app.cli.add_command(check_redis)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
        }
