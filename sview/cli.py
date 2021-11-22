import click
import datetime

from flask import current_app
from flask.cli import with_appcontext

from .resources import try_run_caching_job
from .queries import PRECACHED_RESOURCES
from .queries import PERIODS
from .queries import get_cached_data_key
from .queries import REDIS_CACHE_PREFIX
from .queries import REDIS_REFRESH_PREFIX
from .queries import REDIS_JOB_PREFIX


from .extensions import redis
from .extensions import rq


@click.command()
@with_appcontext
def view_jobs():
    """Clear Redis cache"""
    queue = rq.get_queue()
    job_handler_keys = redis.keys(f"{REDIS_JOB_PREFIX}*")
    for job_handler_key in job_handler_keys:

        job_id = redis.get(job_handler_key)
        if not job_id:
            continue

        # The job was recently deployed. We should try to fetch it.
        job_id = job_id.decode("UTF-8")
        job_ttl = redis.ttl(job_handler_key)
        job = queue.fetch_job(job_id)

        (_, query_name, period_name) = job_handler_key.decode().split(";")
        if not job:  # The job already finished or was cleared
            click.echo(
                f"{query_name:>38s} {period_name:<3s} is removed  "
                f"(id={job_id}, handler_ttl={job_ttl})"
            )
            continue

        # The job was succesfully fetched. We should inspect it's state.
        job_status = job.get_status()
        if job.worker_name:  # The job is assigned to a worker
            execution_time = datetime.datetime.utcnow() - job.started_at
            click.echo(
                f"{query_name:>38s} {period_name:<3s} is {job_status:<8s} "
                f"(id={job_id}, handler_ttl={job_ttl}, worker={job.worker_name}, "
                f"execution_time={execution_time})"
            )

        else:
            click.echo(
                f"{query_name:>38s} {period_name:<3s} is {job_status:<8s} "
                f"(id={job_id}, handler_ttl={job_ttl})"
            )


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
def clear_redis():
    """Clear Redis cache"""
    keys = redis.keys(f"{REDIS_CACHE_PREFIX}*")
    for key in keys:
        redis.delete(key)

    click.echo(f"Cleared {len(keys)} keys")

    keys = redis.keys(f"{REDIS_REFRESH_PREFIX}*")
    for key in keys:
        redis.delete(key)

    click.echo(f"Cleared {len(keys)} refresh timeouts")


@click.command()
@with_appcontext
def queue_queries():
    """Add all cached queries to the queue"""
    for period in PERIODS:
        for resource_name in PRECACHED_RESOURCES:
            click.echo(f"Asking for refresh of: {resource_name} / {period}")
            try_run_caching_job(resource_name, {"period": period})


@click.command()
@click.argument("resource_name", nargs=1, required=True)
@click.argument("period", nargs=1, required=True)
@with_appcontext
def queue_query(resource_name, period):
    """Add cached query to the queue"""
    click.echo(f"Asking for refresh of: {resource_name} / {period}")
    try_run_caching_job(resource_name, {"period": period})


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

    _suffixes = ["bytes", "KiB", "MiB", "GiB", "TiB", "PiB", "EiB", "ZiB", "YiB"]
    order = int(log2(size) / 10) if size else 0
    return "{:.4g} {}".format(size / (1 << (order * 10)), _suffixes[order])


def register_cli_commands(app):
    app.cli.add_command(view_jobs)
    app.cli.add_command(clear_cache)
    app.cli.add_command(queue_queries)
    app.cli.add_command(queue_query)
    app.cli.add_command(check_redis)
    app.cli.add_command(clear_redis)
