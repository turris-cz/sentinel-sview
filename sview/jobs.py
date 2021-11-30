import simplejson

from flask import current_app

from .extensions import redis, rq
from .data_helpers import process_query
from .resources_tools import ResourceToolbox
from .tasks import JOB_TIMEOUT

USER_TTL = 120  # Seconds


@rq.job(result_ttl=10, timeout=JOB_TIMEOUT)
def cache_resource(resource_name, resource_period, params):
    """Precache the most used and default resources"""
    resource = ResourceToolbox(resource_name, resource_period, params=params)
    current_app.logger.debug("Fetching resource %s", resource.name)
    resource_data = process_query(resource.get_query(), resource.get_query_params())

    post_process = resource.query.get("post_process")
    if post_process and callable(post_process):
        # This is experimental feature
        # It would be nice to have better interface
        returned = post_process(resource_data)
        if returned:
            resource_data = returned

    ttl = resource_period["cache_ttl"]
    if "token" in resource.params:
        ttl = min(ttl, USER_TTL)  # Do not cache user-specific resources for long

    redis.set(resource.cached_data_key, simplejson.dumps(resource_data), ex=ttl)
