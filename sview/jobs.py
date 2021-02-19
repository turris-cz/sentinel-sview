import json

from .extensions import redis, rq

from .data_helpers import process_query, precached_data_key
from .job_helpers import mark_data_with_found

from .queries import PERIODS, RESOURCE_QUERIES


@rq.job(result_ttl=10, timeout=600)
def precache_resource(resource_name, period):
    """ Precache the most used and default resources
    """
    params = {
        "start": PERIODS[period]["flux_start"],
        "window": PERIODS[period]["flux_window"],
    }

    params.update(RESOURCE_QUERIES[resource_name].get("params", {}))

    resource = process_query(
        RESOURCE_QUERIES[resource_name]["query"],
        params=params,
        post_process=RESOURCE_QUERIES[resource_name].get("post_process")
    )

    redis.set(precached_data_key(resource_name, period), json.dumps(resource))


@rq.job(result_ttl=300)
def query_resource(resource_name=None, period="1y", **kwargs):
    """ Just a job shell around process_query() function
    """
    kwargs.update({
        "start": PERIODS[period]["flux_start"],
        "window": PERIODS[period]["flux_window"],
    })
    kwargs.update(RESOURCE_QUERIES[resource_name].get("params", {}))
    return process_query(
        RESOURCE_QUERIES[resource_name]["query"],
        params=kwargs,
        post_process=RESOURCE_QUERIES[resource_name].get("post_process")
    )
