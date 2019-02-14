from .extensions import rq
from .data_helpers import get_and_store

from .queries import QUERIES


@rq.job
def load_data_from_template(resource_name):
    get_and_store(resource_name, QUERIES[resource_name])
