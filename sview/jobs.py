from .extensions import rq
from .data_helpers import get_and_store

from .queries import QUERIES


@rq.job(result_ttl=10)
def load_data_from_template(resource_name):
    get_and_store(resource_name, QUERIES[resource_name]["query"], QUERIES[resource_name]["params"])
