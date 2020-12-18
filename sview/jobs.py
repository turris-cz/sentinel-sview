from .extensions import rq

from .data_helpers import get_and_store, process_query
from .job_helpers import mark_data_with_found

from .queries import PRECACHED_QUERIES

from .queries.flux.attackers import attackers_activity_graph

from .queries.flux.passwords import password_activity_graph
from .queries.flux.passwords import logins_of_password


@rq.job(result_ttl=10, timeout=600)
def load_data_from_template(resource_name):
    get_and_store(resource_name,
                  PRECACHED_QUERIES[resource_name]["query"],
                  params=PRECACHED_QUERIES[resource_name].get("params"),
                  post_process=PRECACHED_QUERIES[resource_name].get("post_process"))


@rq.job(result_ttl=300)
def attacker_detail(**kwargs):
    res = {
        "attacker_activity": process_query(attackers_activity_graph, params=kwargs),
    }

    mark_data_with_found(res)

    return res


@rq.job(result_ttl=300)
def password_detail(**kwargs):
    res = {
        "password_during_time": process_query(password_activity_graph, params=kwargs),
        "passwords_logins": process_query(logins_of_password, params=kwargs),
    }

    mark_data_with_found(res)

    return res
