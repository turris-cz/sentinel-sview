from .post_process import as_map_data
from .post_process import as_multiline_graph_data

from .limits import limit_dashboard
from .limits import limit_long
from .limits import limit_plot

from .time import HOUR
from .time import HOUR12
from .time import DAY
from .time import WEEK
from .time import MONTH
from .time import MONTH3
from .time import YEAR

from .time import construct_last_before
from .time import ts_last_midnight_before
from .time import ts_last_3hour_before
from .time import ts_last_half_before
from .time import ts_last_quarter_before
from .time import ts_last_minute_before

from .sql.passwords import top_passwords_by_usages_list
from .sql.passwords import top_usernames_by_usages_list
from .sql.passwords import top_combinations_by_usages_list
from .sql.passwords import top_passwords_by_usages_graph
from .sql.passwords import selected_password_by_usages_graph
from .sql.passwords import logins_of_password_by_usages_list

from .sql.incidents import all_incidents_graph
from .sql.incidents import top_incident_types_by_incidents_list
from .sql.incidents import top_traps_by_incidents_graph
from .sql.incidents import top_actions_by_incidents_graph

from .sql.incidents import all_attackers_graph
from .sql.incidents import top_attackers_by_incidents_list
from .sql.incidents import selected_attacker_incidents_graph
from .sql.incidents import top_countries_by_incidents_list
from .sql.incidents import top_countries_by_attackers_list
from .sql.incidents import all_countries_by_incidents_list
from .sql.incidents import all_countries_by_attackers_list
from .sql.incidents import top_countries_by_attackers_graph
from .sql.incidents import top_countries_by_incidents_graph

from .sql.incidents import my_all_incidents_graph
from .sql.incidents import my_top_countries_by_incidents_graph
from .sql.incidents import my_top_traps_by_incidents_graph

from .sql.ports import all_ports_by_scans_graph
from .sql.ports import top_ports_by_scans_list
from .sql.ports import top_ports_by_scans_graph

REDIS_JOB_PREFIX = "sview_job_id"
REDIS_CACHE_PREFIX = "sview_cached"

KNOWN_PARAMS = {
    "period": "1y",
    "ip": None,
    "password": None,
    "token": None,
}

"""Time periods of displayed data. If you divide period length by length of
flux window, you will get the number of displayed data points. Each period has
defined cache TTL. It seems reasonable for TTL to be half a length of flux
window. Cache TTL is defined in seconds and should be used on both server and
client sides.
"""
DEFAULT_PERIOD = "1y"
PERIODS = {
    "1h": {
        "label": "Hour",
        "bucket": "1 minute",
        "cache_ttl": 30,
        "get_start": construct_last_before(ts_last_minute_before, before=HOUR),
        "get_finish": construct_last_before(ts_last_minute_before),
    },
    "12h": {
        "label": "12 Hours",
        "bucket": "15 minutes",
        "cache_ttl": 450,
        "get_start": construct_last_before(ts_last_quarter_before, before=HOUR12),
        "get_finish": construct_last_before(ts_last_quarter_before),
    },
    "1d": {
        "label": "Day",
        "bucket": "30 minutes",
        "cache_ttl": 900,
        "get_start": construct_last_before(ts_last_half_before, before=DAY),
        "get_finish": construct_last_before(ts_last_half_before),
    },
    "1w": {
        "label": "Week",
        "bucket": "3 hours",
        "cache_ttl": 5400,
        "get_start": construct_last_before(ts_last_3hour_before, before=WEEK),
        "get_finish": construct_last_before(ts_last_3hour_before),
    },
    "1m": {
        "label": "Month",
        "bucket": "1 day",
        "cache_ttl": 432000,
        "get_start": construct_last_before(ts_last_midnight_before, before=MONTH),
        "get_finish": construct_last_before(ts_last_midnight_before),
    },
    "3m": {
        "label": "3 Months",
        "bucket": "2 days",
        "cache_ttl": 864000,
        "get_start": construct_last_before(ts_last_midnight_before, before=MONTH3),
        "get_finish": construct_last_before(ts_last_midnight_before),
    },
    "1y": {
        "label": "Year",
        "bucket": "14 days",
        "cache_ttl": 302400,
        "get_start": construct_last_before(ts_last_midnight_before, before=YEAR),
        "get_finish": construct_last_before(ts_last_midnight_before),
    },
}


RESOURCE_QUERIES = {
    "all_incidents_graph": {
        "query": all_incidents_graph,
    },
    "my_all_incidents_graph": {
        "query": my_all_incidents_graph,
    },
    "all_ports_by_scans_graph": {
        "query": all_ports_by_scans_graph,
    },
    "top_passwords_by_usages_list": {
        "query": top_passwords_by_usages_list,
        "params": {"limit": limit_dashboard},
    },
    "top_passwords_by_usages_list_long": {
        "query": top_passwords_by_usages_list,
        "params": {"limit": limit_long},
    },
    "top_usernames_by_usages_list": {
        "query": top_usernames_by_usages_list,
        "params": {"limit": limit_dashboard},
    },
    "top_usernames_by_usages_list_long": {
        "query": top_usernames_by_usages_list,
        "params": {"limit": limit_long},
    },
    "top_ports_by_scans_list_long": {
        "query": top_ports_by_scans_list,
        "params": {"limit": limit_long},
    },
    "top_countries_by_incidents_list": {
        "query": top_countries_by_incidents_list,
        "params": {"limit": limit_dashboard},
    },
    "top_countries_by_incidents_list_long": {
        "query": top_countries_by_incidents_list,
        "params": {"limit": limit_long},
    },
    "top_countries_by_attackers_list": {
        "query": top_countries_by_attackers_list,
        "params": {"limit": limit_dashboard},
    },
    "top_countries_by_attackers_list_long": {
        "query": top_countries_by_attackers_list,
        "params": {"limit": limit_long},
    },
    "top_attackers_by_incidents_list_long": {
        "query": top_attackers_by_incidents_list,
        "params": {"limit": limit_long},
    },
    "top_combinations_by_usages_list_long": {
        "query": top_combinations_by_usages_list,
        "params": {"limit": limit_long},
    },
    "top_incident_types_by_incidents_list": {
        "query": top_incident_types_by_incidents_list,
        "params": {"limit": limit_dashboard},
    },
    "all_countries_by_incidents_list": {
        "query": all_countries_by_incidents_list,
        "post_process": lambda d: as_map_data(d, "country", "count"),
    },
    "all_countries_by_attackers_list": {
        "query": all_countries_by_attackers_list,
        "post_process": lambda d: as_map_data(d, "country", "count"),
    },
    "all_attackers_graph": {
        "query": all_attackers_graph,
    },
    "top_countries_by_attackers_graph": {
        "query": top_countries_by_attackers_graph,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(
            d, "bucket", "count", "country"
        ),
    },
    "top_countries_by_incidents_graph": {
        "query": top_countries_by_incidents_graph,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(
            d, "bucket", "count", "country"
        ),
    },
    "top_traps_by_incidents_graph": {
        "query": top_traps_by_incidents_graph,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(
            d, "bucket", "count", "source"
        ),
    },
    "my_top_countries_by_incidents_graph": {
        "query": my_top_countries_by_incidents_graph,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(
            d, "bucket", "count", "country"
        ),
    },
    "my_top_traps_by_incidents_graph": {
        "query": my_top_traps_by_incidents_graph,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(
            d, "bucket", "count", "source"
        ),
    },
    "top_actions_by_incidents_graph": {
        "query": top_actions_by_incidents_graph,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(
            d, "bucket", "count", "action"
        ),
    },
    "top_ports_by_scans_graph": {
        "query": top_ports_by_scans_graph,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(d, "bucket", "count", "port"),
    },
    "top_passwords_by_usages_graph": {
        "query": top_passwords_by_usages_graph,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(
            d, "bucket", "count", "password"
        ),
    },
    "selected_attacker_incidents_graph": {
        "query": selected_attacker_incidents_graph,
    },
    "selected_password_by_usages_graph": {
        "query": selected_password_by_usages_graph,
    },
    "logins_of_password_by_usages_list": {
        "query": logins_of_password_by_usages_list,
    },
}


PRECACHED_RESOURCES = [
    ("top_passwords_by_usages_list", {"period": "1y"}),
    ("top_passwords_by_usages_list_long", {"period": "1y"}),
    ("top_usernames_by_usages_list", {"period": "1y"}),
    ("top_usernames_by_usages_list_long", {"period": "1y"}),
    ("top_countries_by_attackers_list", {"period": "1y"}),
    ("top_countries_by_attackers_list_long", {"period": "1y"}),
    ("top_countries_by_incidents_list", {"period": "1y"}),
    ("top_countries_by_incidents_list_long", {"period": "1y"}),
    ("top_attackers_by_incidents_list_long", {"period": "1y"}),
    ("top_combinations_by_usages_list_long", {"period": "1y"}),
    ("all_countries_by_attackers_list", {"period": "1y"}),
    ("all_countries_by_incidents_list", {"period": "1y"}),
    ("all_attackers_graph", {"period": "1y"}),
    ("top_countries_by_attackers_graph", {"period": "1y"}),
    ("top_passwords_by_usages_graph", {"period": "1y"}),
]


def get_job_handler_key(resource_name, params):
    return "{};{}".format(
        REDIS_JOB_PREFIX,
        ";".join(
            [resource_name]
            + [v for k, v in params.items() if k in KNOWN_PARAMS and v is not None]
        ),
    )


def get_cached_data_key(resource_name, params):
    return "{};{}".format(
        REDIS_CACHE_PREFIX,
        ";".join(
            [resource_name]
            + [v for k, v in params.items() if k in KNOWN_PARAMS and v is not None]
        ),
    )
