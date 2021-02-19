from flask import jsonify
import json

from .data_helpers import precached_data_key
from .exceptions import ResourceError
from .extensions import redis
from .job_helpers import run_job
from .jobs import query_resource
from .queries import PERIODS, RESOURCE_QUERIES

KNOWN_PARAMS = {
    "period": "1y",
}

def job_handler(resource_name, params):
    return ":".join([resource_name] + list(params.values()))


def get_resource(resource_name, params):
    """ Return a cached resource or start a job to query it.
    Return either requested resource or None when it is not ready yet.
    Raise an exception in case of invalid resource or invalid parameters.
    """

    if resource_name not in RESOURCE_QUERIES:
        raise ResourceError("Unknown resource")

    if params["period"] not in PERIODS:
        raise ResourceError("Not a valid period")

    precached_result = redis.get(precached_data_key(resource_name, params["period"]))
    if precached_result:
        resource = json.loads(precached_result.decode("utf-8"))
        return resource

    resource, _ = run_job(
        job_handler(resource_name, params),
        query_resource,
        resource_name=resource_name,
        **params
    )

    return resource
