from .extensions import rq
from .data_helpers import get_and_store

from .queries import QUERIES


@rq.job(result_ttl=10)
def load_data_from_template(resource_name):
    get_and_store(resource_name,
                  QUERIES[resource_name]["query"],
                  params=QUERIES[resource_name].get("params"),
                  post_process=QUERIES[resource_name].get("post_process"))
