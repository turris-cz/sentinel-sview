import json

from .exceptions import ResourceError
from .extensions import redis, rq
from .jobs import cache_resource
from .queries import PERIODS
from .queries import RESOURCE_QUERIES
from .queries import get_cached_data_key
from .queries import get_job_handler_key
from .rlimit import rlimit

USER_SPECIFIC_RESOURCES = (
    "my_all_incidents_graph",
    "my_top_countries_by_incidents_graph",
    "my_top_traps_by_incidents_graph",
)


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
        return []

    precached_result = redis.get(get_cached_data_key(resource_name, params))
    if precached_result:
        resource = json.loads(precached_result.decode("utf-8"))
        return resource

    _run_caching_job(resource_name, params)


def _run_caching_job(resource_name, params):
    """Enqueue a job or check its result when it is already enqueued.
    Return either job.result when the job already finished or
    None when it is still pending.
    """
    job_handler_key = get_job_handler_key(resource_name, params)

    @rlimit
    def _queue_job():
        job = cache_resource.queue(resource_name, params)
        redis.set(job_handler_key, job.id, ex=job.result_ttl)

    job_id = redis.get(job_handler_key)
    if job_id:
        job_id = job_id.decode("UTF-8")
    else:
        _queue_job()
        return

    job = rq.get_queue().fetch_job(job_id)
    if not job:
        _queue_job()
        return

    # TODO: Check whether the job is in fail state, but there's probably
    # no point in notifying the client what exactly went wrong
