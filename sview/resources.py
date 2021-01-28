from flask import jsonify
import json

from .data_helpers import precached_data_key
from .exceptions import ResourceError
from .extensions import redis
from .job_helpers import run_job
from .jobs import query_resource
from .queries import PERIODS, RESOURCE_QUERIES


def get_resource(resource_name, period="1y"):
    """ Return a cached resource or start a job to query it.
    Return either requested resource or None when it is not ready yet.
    Raise an exception in case of invalid resource or invalid parameters.
    """

    if resource_name not in RESOURCE_QUERIES:
        raise ResourceError("Unknown resource")

    if period not in PERIODS:
        raise ResourceError("Not a valid period")

    precached_result = redis.get(precached_data_key(resource_name, period))
    if precached_result:
        resource = json.loads(precached_result.decode("utf-8"))
        return resource

    resource, _ = run_job(
        "{}:{}".format(resource_name, period),
        query_resource,
        resource_name=resource_name,
        period=period
    )

    return resource
