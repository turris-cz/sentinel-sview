import click
from flask import current_app
from flask.cli import with_appcontext

from .statistics import suggest_aggregation
from .statistics import Aggregation
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
    click.echo("Resource caching jobs:")
    for job_info in Resource.inspect_jobs():
        click.echo(job_info)

    click.echo("")
    click.echo("Aggregation jobs:")
    for job_info in Aggregation.inspect_jobs():
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
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    help="Do not clear anything, just print what would be cleared",
)
def clear_redis_cache(dry_run=False):
    """Clear cached resources and their timeouts from redis"""
    for info in Resource.inspect_cache(clear=True, dry_run=dry_run):
        click.echo(info)

    click.echo("")
    for info in Resource.inspect_timeouts(clear=True, dry_run=dry_run):
        click.echo(info)


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

    for result in suggest_caching_period("6h", dry_run=dry_run):
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
    for info in Resource.inspect_cache():
        click.echo(info)


@click.command()
@with_appcontext
def view_timeouts():
    """View resource refresh timeouts and aggregation timeouts"""
    click.echo("Resource refresh timeouts: (refresh is allowed after timeout expires)")
    for timeout_info in Resource.inspect_timeouts():
        click.echo(timeout_info)

    click.echo("")
    click.echo("Aggregation timeouts: (aggregation is allowed after timeout expires)")
    for timeout_info in Aggregation.inspect_timeouts():
        click.echo(timeout_info)


@click.command()
@click.argument("task", nargs=1, required=True)
@click.argument("period", nargs=1, required=True)
@click.option(
    "-d",
    "--dry-run",
    is_flag=True,
    help="Do not clear anything, just print what would be cleared",
)
@with_appcontext
def clear_timeouts(task, period, dry_run=False):
    """Clear resource refresh or aggregation timeouts"""
    available_tasks = {
        "aggregation": Aggregation,
        "resource": Resource,
    }
    task = available_tasks.get(task)
    if task is None:
        click.echo(f"Task must be one of {[name for name in available_tasks]}")
        return

    if period not in task.AVAILABLE_PERIODS:
        click.echo(
            f"Period must be one of: {[name for name in task.AVAILABLE_PERIODS]}"
        )
        return

    for timeout_info in Resource.inspect_timeouts(period_name=period, clear=True, dry_run=dry_run):
        click.echo(timeout_info)


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
