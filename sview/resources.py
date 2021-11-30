import json

from .exceptions import ResourceError
from .extensions import redis
from .jobs import cache_resource, JOB_TIMEOUT
from .job_helpers import JobState
from .queries import PERIODS
from .queries import RESOURCE_QUERIES
from .queries import get_cached_data_key
from .queries import get_job_handler_key
from .queries import get_refresh_timeout_key
from .rlimit import rate_limit_reached

USER_SPECIFIC_RESOURCES = (
    "my_all_incidents_graph",
    "my_top_countries_by_incidents_graph",
    "my_top_traps_by_incidents_graph",
)

REDIS_PLACEHOLDER = "1"  # Shall only return logical true


def get_resource(resource_name, params):
    """Return a cached resource or start a job to query & cache it.
    Return either requested resource or None when it is not ready yet.
    Raise an exception in case of invalid resource or invalid parameters.
    """

    if resource_name not in RESOURCE_QUERIES:
        raise ResourceError(f"Unknown resource '{resource_name}'")

    if params["period"] not in PERIODS:
        raise ResourceError("Not a valid period")

    if resource_name in USER_SPECIFIC_RESOURCES and "token" not in params:
        return RESOURCE_QUERIES[resource_name].get("empty_response", [])

    try_run_caching_job(resource_name, params, rlimit_checking=True)

    precached_result = redis.get(get_cached_data_key(resource_name, params))
    if precached_result:
        resource = json.loads(precached_result.decode("utf-8"))
        return resource


def try_run_caching_job(resource_name, params, rlimit_checking=False, dry_run=False):
    """Enqueue a job when refresh is allowed or check its result when it is
    already enqueued.
    """
    job_handler_key = get_job_handler_key(resource_name, params)
    refresh_timeout_key = get_refresh_timeout_key(resource_name, params)
    refresh_ttl = redis.ttl(refresh_timeout_key)
    is_time_to_refresh = refresh_ttl <= 0  # -1 for no key, -2 for key with no ttl
    cache_ttl = redis.ttl(get_cached_data_key(resource_name, params))
    cache_is_empty = cache_ttl <= 0  # -1 for no key, -2 for key with no ttl

    def _queue_job():
        if dry_run:
            return

        if rlimit_checking and rate_limit_reached():
            raise ResourceError("Too many requests in row")

        refresh_timeout = PERIODS[params["period"]]["get_refresh_timeout"]()
        job = cache_resource.queue(resource_name, params)
        redis.set(job_handler_key, job.id, ex=JOB_TIMEOUT)
        redis.set(refresh_timeout_key, REDIS_PLACEHOLDER, ex=refresh_timeout)
        return job.id


    job_state = JobState(job_handler_key)
    if not job_state.is_alive() and (
        is_time_to_refresh or cache_is_empty or job_state.is_failed()
    ):
        job_id = _queue_job()
        return (
            f"Queueing cache {resource_name:^38s} {params['period']:>3s} "
            f"(refresh_ttl={refresh_ttl}, cache_ttl={cache_ttl}, "
            f"status={job_state.status}) with id={job_id}"
        )

    return (
        f"Skipping cache {resource_name:^38s} {params['period']:>3s} "
        f"(refresh_ttl={refresh_ttl}, cache_ttl={cache_ttl}, "
        f"status={job_state.status}, job_id={job_state.id})"
    )
