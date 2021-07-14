import json

from .extensions import redis, rq
from .data_helpers import process_query
from .queries import PERIODS
from .queries import get_cached_data_key


@rq.job(result_ttl=10, timeout=600)
def cache_resource(resource_name, params):
    """ Precache the most used and default resources
    """
    resource = process_query(resource_name, params)

    redis.set(get_cached_data_key(resource_name, params), json.dumps(resource), ex=PERIODS[params["period"]]["cache_ttl"])
