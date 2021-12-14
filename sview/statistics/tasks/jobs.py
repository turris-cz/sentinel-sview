import simplejson

from flask import current_app

from ...extensions import redis, rq

from .aggregation_tools import AggregationToolbox
from .data_helpers import process_query
from .resources_tools import ResourceToolbox
from .tasks import JOB_TIMEOUT


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

    redis.set(
        resource.cached_data_key,
        simplejson.dumps(resource_data),
        ex=resource.get_cache_ttl(),
    )


@rq.job(result_ttl=10, timeout=JOB_TIMEOUT)
def aggregate(data_type, aggregation_period, params):
    aggregation = AggregationToolbox(data_type, aggregation_period)
    process_query(aggregation.get_query(), aggregation.get_query_params())
