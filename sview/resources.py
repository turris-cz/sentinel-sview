import json

from .exceptions import ResourceError
from .extensions import redis, rq
from .jobs import cache_resource, JOB_TIMEOUT
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

JOB_STATUS_STARTED = "started"
JOB_STATUS_QUEUED = "queued"
JOB_STATUS_FAILED = "failed"
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


def try_run_caching_job(resource_name, params, rlimit_checking=False):
    """Enqueue a job when refresh is allowed or check its result when it is
    already enqueued.
    """
    job_handler_key = get_job_handler_key(resource_name, params)
    refresh_timeout_key = get_refresh_timeout_key(resource_name, params)
    is_time_to_refresh = not redis.exists(
        get_refresh_timeout_key(resource_name, params)
    )
    cache_is_empty = not redis.exists(get_cached_data_key(resource_name, params))

    def _queue_job():
        if rlimit_checking and rate_limit_reached():
            raise ResourceError("Too many requests in row")

        refresh_timeout = PERIODS[params["period"]]["get_refresh_timeout"]()
        job = cache_resource.queue(resource_name, params)
        redis.set(job_handler_key, job.id, ex=JOB_TIMEOUT)
        redis.set(refresh_timeout_key, REDIS_PLACEHOLDER, ex=refresh_timeout)

    job_id = redis.get(job_handler_key)

    if not job_id:  # It seems that there should be no job under processing.
        if is_time_to_refresh or cache_is_empty:
            _queue_job()
        return

    # The job was recently deployed. We should try to fetch it.
    job_id = job_id.decode("UTF-8")
    job = rq.get_queue().fetch_job(job_id)

    if not job:  # The job already finished or was cleared
        if is_time_to_refresh or cache_is_empty:
            _queue_job()
        return

    # The job was succesfully fetched. We should inspect it's state.
    job_status = job.get_status()

    if job_status in [JOB_STATUS_STARTED, JOB_STATUS_QUEUED]:
        return

    if job_status == JOB_STATUS_FAILED:
        _queue_job()
        return
