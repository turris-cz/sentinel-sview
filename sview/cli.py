import click

from flask import current_app
from flask.cli import with_appcontext

from .jobs import cache_resource
from .queries import PRECACHED_RESOURCES
from .queries import get_cached_data_key

from .extensions import redis


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
    for resource_request in PRECACHED_RESOURCES:
        click.echo("Queuing: {}".format(resource_request))
        cache_resource.queue(*resource_request)


@click.command()
@click.argument("resource_name", nargs=1, required=True)
@click.argument("period", nargs=1, required=True)
@with_appcontext
def queue_query(resource_name, period):
    """Add cached query to the queue"""
    click.echo("Queuing: {}".format((resource_name, period)))
    cache_resource.queue(resource_name, {"period": period})


@click.command()
@with_appcontext
def check_redis():
    """Check state of data in redis"""
    size = 0
    available = []
    missing = []

    for resource_request in PRECACHED_RESOURCES:
        data = redis.get(get_cached_data_key(*resource_request))
        if data:
            available.append(resource_request)
            size += len(data)
        else:
            missing.append(resource_request)

    if available:
        click.echo("Stored keys:")
        for resource_request in available:
            click.echo("  - {}".format(get_cached_data_key(*resource_request)))
    if missing:
        click.echo("Missing keys:")
        for resource_request in missing:
            click.echo("  - {}".format(get_cached_data_key(*resource_request)))
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
