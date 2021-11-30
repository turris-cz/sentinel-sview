import click
from flask import current_app
from flask.cli import with_appcontext

from .job_helpers import inspect_jobs
from .resources import suggest_caching
from .resources import suggest_caching_period
from .resources import Resource
from .extensions import redis


@click.command()
@with_appcontext
def view_jobs():
    for job_info in inspect_jobs(Resource.REDIS_JOB_PREFIX):
        click.echo(job_info)


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
def clear_redis_cache():
    """Clear Redis cache"""
    keys = redis.keys(f"{Resource.REDIS_CACHE_PREFIX}*")
    for key in keys:
        redis.delete(key)

    click.echo(f"Cleared {len(keys)} keys")

    keys = redis.keys(f"{Resource.REDIS_REFRESH_TO_PREFIX}*")
    for key in keys:
        redis.delete(key)

    click.echo(f"Cleared {len(keys)} refresh timeouts")


@click.command()
@with_appcontext
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    help="Do not queue anything, just print what would be queued",
)
def refresh(dry_run=False):
    """Suggest refresh of all outdated resources"""
    for result in suggest_caching_period("1h", dry_run=dry_run):
        click.echo(result)

    for result in suggest_caching_period("12h", dry_run=dry_run):
        click.echo(result)
    for result in suggest_caching_period("1d", dry_run=dry_run):
        click.echo(result)

    for result in suggest_caching_period("1w", dry_run=dry_run):
        click.echo(result)

    for result in suggest_caching_period("1m", dry_run=dry_run):
        click.echo(result)
    for result in suggest_caching_period("3m", dry_run=dry_run):
        click.echo(result)
    for result in suggest_caching_period("1y", dry_run=dry_run):
        click.echo(result)


@click.command()
@click.argument("resource_name", nargs=1, required=True)
@click.argument("period", nargs=1, required=True)
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    help="Do not queue anything, just print what would be queued",
)
@with_appcontext
def refresh_resource(resource_name, period, dry_run=False):
    """Suggest refresh of a resource"""
    click.echo(suggest_caching(resource_name, {"period": period}, dry_run=dry_run))


@click.command()
@with_appcontext
def view_redis_cache():
    keys = redis.keys(f"{Resource.REDIS_CACHE_PREFIX}*")
    size = 0
    for key in keys:
        data = redis.get(key)
        ttl = redis.ttl(key)
        key = key.decode()
        if data:
            click.echo(
                f"{key:<55s} ttl={ttl:<6} size={_human_readable_bytes(len(data))}"
            )
            size += len(data)

    click.echo("")
    click.echo("Cached resources occupy:  {}".format(_human_readable_bytes(size)))


def _human_readable_bytes(size):
    from math import log2

    _suffixes = ["bytes", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
    order = int(log2(size) / 10) if size else 0
    return "{:.4g} {}".format(size / (1 << (order * 10)), _suffixes[order])


def register_cli_commands(app):
    app.cli.add_command(view_jobs)
    app.cli.add_command(clear_cache)
    app.cli.add_command(refresh)
    app.cli.add_command(refresh_resource)
    app.cli.add_command(view_redis_cache)
    app.cli.add_command(clear_redis_cache)
