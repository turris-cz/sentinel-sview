from .extensions import rq

from .data_helpers import get_and_store, process_query
from .job_helpers import check_and_mark_data_with_found

from .queries import QUERIES
from .queries import _attacker_activity_during_time, _attacker_passwords


@rq.job(result_ttl=10)
def load_data_from_template(resource_name):
    get_and_store(resource_name,
                  QUERIES[resource_name]["query"],
                  params=QUERIES[resource_name].get("params"),
                  post_process=QUERIES[resource_name].get("post_process"))


@rq.job(result_ttl=300)
def attacker_detail(**kwargs):
    res = {
        "attacker_activity": process_query(_attacker_activity_during_time, params=kwargs),
        "attacker_passwords": process_query(_attacker_passwords, params=kwargs),
    }

    check_and_mark_data_with_found(res)

    return res
