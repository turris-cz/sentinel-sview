from .extensions import rq

from .data_helpers import get_and_store, process_query
from .job_helpers import mark_data_with_found

from .queries import PRECACHED_QUERIES

from .queries.post_process import as_map_data

from .queries.sql.attackers import attackers_activity_graph
from .queries.sql.attackers import attackers_of_password

from .queries.sql.passwords import password_activity_graph
from .queries.sql.passwords import logins_of_password
from .queries.sql.passwords import passwords_of_attacker

from .queries.sql.tests import _day_country_attackers, _day_ip_attackers


@rq.job(result_ttl=10)
def load_data_from_template(resource_name):
    get_and_store(resource_name,
                  PRECACHED_QUERIES[resource_name]["query"],
                  params=PRECACHED_QUERIES[resource_name].get("params"),
                  post_process=PRECACHED_QUERIES[resource_name].get("post_process"))


@rq.job(result_ttl=300)
def attacker_detail(**kwargs):
    res = {
        "attacker_activity": process_query(attackers_activity_graph, params=kwargs),
        "attacker_passwords": process_query(passwords_of_attacker, params=kwargs),
    }

    mark_data_with_found(res)

    return res


@rq.job(result_ttl=300)
def day_detail(**kwargs):
    res = {
        "countries_map": process_query(_day_country_attackers, params=kwargs,
                                       post_process=lambda d: as_map_data(d, "country", "count")),
        "attackers": process_query(_day_ip_attackers, params=kwargs),
    }

    mark_data_with_found(res)

    return res


@rq.job(result_ttl=300)
def password_detail(**kwargs):
    res = {
        "password_during_time": process_query(password_activity_graph, params=kwargs),
        "password_by_attackers": process_query(attackers_of_password, params=kwargs),
        "passwords_logins": process_query(logins_of_password, params=kwargs),
    }

    mark_data_with_found(res)

    return res
