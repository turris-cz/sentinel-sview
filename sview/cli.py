import click
from flask import current_app
from flask.cli import with_appcontext

from .extensions import redis
from .statistics import suggest_aggregation
from .statistics import Aggregation
from .statistics import inspect_jobs
from .statistics import RESOURCE_QUERIES
from .statistics import suggest_caching
from .statistics import suggest_caching_period
from .statistics import Resource
from .statistics import QUARTERLY_PERIOD, HOURLY_PERIOD, DAILY_PERIOD
from .statistics import PERIODS, AGGREGATION_PERIODS
from .statistics.tasks.periods.time import DAY


@click.command()
@with_appcontext
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    help="Do not queue anything, just print what would be queued",
)
@click.argument("period", nargs=1, required=True)
def migrate_period(period, dry_run=False):
    """Suggest extended aggregation supposed for development"""
    available_periods = {
        "quarterly": {**QUARTERLY_PERIOD, **{"display_interval": DAY * 9}},
        "hourly": {**HOURLY_PERIOD, **{"display_interval": DAY * 8}},
        "daily": {**DAILY_PERIOD, **{"display_interval": DAY * 7}},
    }
    if period not in available_periods:
        click.echo(f"Period must be one of: {[name for name in available_periods]}")
        return

    click.echo(
        suggest_aggregation("incidents", available_periods[period], dry_run=dry_run)
    )
    click.echo(
        suggest_aggregation("passwords", available_periods[period], dry_run=dry_run)
    )
    click.echo(suggest_aggregation("ports", available_periods[period], dry_run=dry_run))


@click.command()
@with_appcontext
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    help="Do not queue anything, just print what would be queued",
)
@click.argument("period", nargs=1, required=True)
def aggregate_period(period, dry_run=False):
    """Suggest aggregation of a period"""
    if period not in AGGREGATION_PERIODS:
        click.echo(f"Period must be one of: {[name for name in AGGREGATION_PERIODS]}")
        return

    click.echo(
        suggest_aggregation("incidents", AGGREGATION_PERIODS[period], dry_run=dry_run)
    )
    click.echo(
        suggest_aggregation("passwords", AGGREGATION_PERIODS[period], dry_run=dry_run)
    )
    click.echo(
        suggest_aggregation("ports", AGGREGATION_PERIODS[period], dry_run=dry_run)
    )


@click.command()
@with_appcontext
def view_jobs():
    """View all resource and aggregation jobs"""
    for job_info in inspect_jobs(Resource.REDIS_JOB_PREFIX):
        click.echo(job_info)

    for job_info in inspect_jobs(Aggregation.REDIS_JOB_PREFIX):
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
    """Clear cached resources and their timeouts from redis"""
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
    """Suggest aggregation and refresh of all resources"""
    for result in suggest_caching_period("1h", dry_run=dry_run):
        click.echo(result)

    click.echo(suggest_aggregation("incidents", QUARTERLY_PERIOD, dry_run=dry_run))
    click.echo(suggest_aggregation("passwords", QUARTERLY_PERIOD, dry_run=dry_run))
    click.echo(suggest_aggregation("ports", QUARTERLY_PERIOD, dry_run=dry_run))

    click.echo(suggest_aggregation("incidents", HOURLY_PERIOD, dry_run=dry_run))
    click.echo(suggest_aggregation("passwords", HOURLY_PERIOD, dry_run=dry_run))
    click.echo(suggest_aggregation("ports", HOURLY_PERIOD, dry_run=dry_run))

    click.echo(suggest_aggregation("incidents", DAILY_PERIOD, dry_run=dry_run))
    click.echo(suggest_aggregation("passwords", DAILY_PERIOD, dry_run=dry_run))
    click.echo(suggest_aggregation("ports", DAILY_PERIOD, dry_run=dry_run))

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
@click.argument("period", nargs=1, required=True)
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    help="Do not queue anything, just print what would be queued",
)
@with_appcontext
def cache_period(period, dry_run=False):
    """Suggest refresh of all cached resources with period"""
    if period not in PERIODS:
        click.echo(f"Period must be one of: {[name for name in PERIODS]}")
        return

    for result in suggest_caching_period(period, dry_run=dry_run):
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
def cache_resource(resource_name, period, dry_run=False):
    """Suggest refresh of a resource"""
    if resource_name not in RESOURCE_QUERIES:
        click.echo(f"Resource must be one of: {[name for name in RESOURCE_QUERIES]}")
        return
    if period not in PERIODS:
        click.echo(f"Period must be one of: {[name for name in PERIODS]}")
        return
    click.echo(suggest_caching(resource_name, period, dry_run=dry_run))


@click.command()
@with_appcontext
def view_redis_cache():
    """View all resource cache keys with cache ttl and size"""
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


@click.command()
@with_appcontext
def view_timeouts():
    """View resource refresh timeouts and aggregation timeouts"""
    click.echo("Resource refresh timeouts: (refresh is allowed after timeout expires)")
    keys = redis.keys(f"{Resource.REDIS_REFRESH_TO_PREFIX}*")
    timeout_logs = []
    for key in keys:
        ttl = redis.ttl(key)
        key = key.decode()
        key_parts = key.split(";")
        timeout_log = {
            "ttl": ttl,
            "name": key_parts[1],
            "period": key_parts[2],
            "params": key_parts[3:],  # optional - like ip or device_token
            "index": PERIODS[key_parts[2]]["index"],  # for sorting
        }
        timeout_logs.append(timeout_log)

    for log in sorted(timeout_logs, key=lambda item: item.get("index")):
        click.echo(
            f"{log['name']:<40s} {log['period']:<9s} ttl={log['ttl']:<6} params={log['params']}"
        )

    click.echo("")
    click.echo("Aggregation timeouts: (aggregation is triggered after timeout expires)")
    keys = redis.keys(f"{Aggregation.REDIS_REFRESH_TO_PREFIX}*")
    timeout_logs = []
    for key in keys:
        ttl = redis.ttl(key)
        key = key.decode()
        key_parts = key.split(";")
        timeout_log = {
            "ttl": ttl,
            "name": key_parts[1],
            "period": key_parts[2],
            "index": AGGREGATION_PERIODS[key_parts[2]]["index"],  # for sorting
        }
        timeout_logs.append(timeout_log)

    for log in sorted(timeout_logs, key=lambda item: item.get("index")):
        click.echo(f"{log['name']:<40s} {log['period']:<9s} ttl={log['ttl']:<6}")


@click.command()
@click.argument("task", nargs=1, required=True)
@click.argument("period", nargs=1, required=True)
@with_appcontext
def clear_timeouts(task, period):
    """Clear resource refresh or aggregation timeouts"""
    if task not in ["aggregation", "resource"]:
        click.echo(f"Task must be one of 'aggregation', 'resource'")
        return

    if task == "resource":
        if period not in PERIODS:
            click.echo(f"Period must be one of: {[name for name in PERIODS]}")
            return
        keys = redis.keys(f"{Resource.REDIS_REFRESH_TO_PREFIX};*;{period}")
        for key in keys:
            ttl = redis.ttl(key)
            key_parts = key.decode().split(";")
            log = {
                "ttl": ttl,
                "name": key_parts[1],
                "period": key_parts[2],
                "params": key_parts[3:],  # optional - like ip or device_token
            }
            click.echo(
                f"Clearing {log['name']:<40s} {log['period']:<9s} ttl={log['ttl']:<6} params={log['params']}"
            )
            redis.delete(key)

    if task == "aggregation":
        if period not in AGGREGATION_PERIODS:
            click.echo(
                f"Period must be one of: {[name for name in AGGREGATION_PERIODS]}"
            )
            return
        keys = redis.keys(f"{Aggregation.REDIS_REFRESH_TO_PREFIX};*;{period}")
        print(f"{Aggregation.REDIS_REFRESH_TO_PREFIX};*;{period}")
        for key in keys:
            ttl = redis.ttl(key)
            key_parts = key.decode().split(";")
            log = {
                "ttl": ttl,
                "name": key_parts[1],
                "period": key_parts[2],
            }
            click.echo(
                f"Clearing {log['name']:<40s} {log['period']:<9s} ttl={log['ttl']:<6}"
            )
            redis.delete(key)


def _human_readable_bytes(size):
    from math import log2

    _suffixes = ["bytes", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
    order = int(log2(size) / 10) if size else 0
    return "{:.4g} {}".format(size / (1 << (order * 10)), _suffixes[order])


def register_cli_commands(app):
    app.cli.add_command(migrate_period)
    app.cli.add_command(aggregate_period)
    app.cli.add_command(view_jobs)
    app.cli.add_command(clear_cache)
    app.cli.add_command(refresh)
    app.cli.add_command(cache_resource)
    app.cli.add_command(cache_period)
    app.cli.add_command(view_redis_cache)
    app.cli.add_command(view_timeouts)
    app.cli.add_command(clear_redis_cache)
    app.cli.add_command(clear_timeouts)
