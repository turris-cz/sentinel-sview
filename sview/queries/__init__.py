from .post_process import as_map_data
from .post_process import as_multiline_graph_data

from .limits import limit_dashboard
from .limits import limit_long
from .limits import limit_plot

from .sql.passwords import top_passwords
from .sql.passwords import top_usernames
from .sql.passwords import top_combinations
from .sql.passwords import top_passwords_popularity
from .sql.passwords import password_activity_graph
from .sql.passwords import logins_of_password

from .sql.incidents import all_incidents_graph
from .sql.incidents import top_incident_types
from .sql.incidents import incidents_by_source_trends
from .sql.incidents import incidents_by_action_trends

from .sql.incidents import attackers_by_day
from .sql.incidents import attacker_ips
from .sql.incidents import attackers_activity_graph
from .sql.incidents import top_countries_by_incidents_table
from .sql.incidents import top_countries_by_attackers_table
from .sql.incidents import incidents_map
from .sql.incidents import attackers_map
from .sql.incidents import top_countries_trends
from .sql.incidents import incidents_by_country_trends

from .sql.incidents import my_incidents_graph
from .sql.incidents import my_incidents_by_country_trends
from .sql.incidents import my_incidents_by_source_trends

from .sql.ports import all_scans_graph
from .sql.ports import top_ports
from .sql.ports import port_trends

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
        "interval": "1 hour",
        "bucket": "1 minute",
        "cache_ttl": 30,
    },
    "12h": {
        "label": "12 Hours",
        "interval": "12 hours",
        "bucket": "15 minutes",
        "cache_ttl": 450,
    },
    "1d": {
        "label": "Day",
        "interval": "1 day",
        "bucket": "30 minutes",
        "cache_ttl": 900,
    },
    "1w": {
        "label": "Week",
        "interval": "7 days",
        "bucket": "3 hours",
        "cache_ttl": 5400,
    },
    "1m": {
        "label": "Month",
        "interval": "1 month",
        "bucket": "1 day",
        "cache_ttl": 432000,
    },
    "3m": {
        "label": "3 Months",
        "interval": "3 months",
        "bucket": "2 days",
        "cache_ttl": 864000,
    },
    "1y": {
        "label": "Year",
        "interval": "1 year",
        "bucket": "14 days",
        "cache_ttl": 302400,
    },
}


RESOURCE_QUERIES = {
    "all_incidents_graph": {
        "query": all_incidents_graph,
    },
    "my_incidents_graph": {
        "query": my_incidents_graph,
    },
    "all_scans_graph": {
        "query": all_scans_graph,
    },
    "top_passwords": {
        "query": top_passwords,
        "params": {"limit": limit_dashboard},
    },
    "top_passwords_long": {
        "query": top_passwords,
        "params": {"limit": limit_long},
    },
    "top_usernames": {
        "query": top_usernames,
        "params": {"limit": limit_dashboard},
    },
    "top_usernames_long": {
        "query": top_usernames,
        "params": {"limit": limit_long},
    },
    "top_ports_long": {
        "query": top_ports,
        "params": {"limit": limit_long},
    },
    "top_countries_by_incidents_table": {
        "query": top_countries_by_incidents_table,
        "params": {"limit": limit_dashboard},
    },
    "top_countries_by_incidents_table_long": {
        "query": top_countries_by_incidents_table,
        "params": {"limit": limit_long},
    },
    "top_countries_by_attackers_table": {
        "query": top_countries_by_attackers_table,
        "params": {"limit": limit_dashboard},
    },
    "top_countries_by_attackers_table_long": {
        "query": top_countries_by_attackers_table,
        "params": {"limit": limit_long},
    },
    "top_ips_long": {
        "query": attacker_ips,
        "params": {"limit": limit_long},
    },
    "top_combinations_long": {
        "query": top_combinations,
        "params": {"limit": limit_long},
    },
    "top_incident_types": {
        "query": top_incident_types,
        "params": {"limit": limit_dashboard},
    },
    "incidents_map": {
        "query": incidents_map,
        "post_process": lambda d: as_map_data(d, "country", "count"),
    },
    "attackers_map": {
        "query": attackers_map,
        "post_process": lambda d: as_map_data(d, "country", "count"),
    },
    "attackers": {
        "query": attackers_by_day,
    },
    "attackers_trends": {
        "query": top_countries_trends,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(d, "day", "count", "country"),
    },
    "incidents_by_country_trends": {
        "query": incidents_by_country_trends,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(d, "day", "count", "country"),
    },
    "incidents_by_source_trends": {
        "query": incidents_by_source_trends,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(d, "day", "count", "source"),
    },
    "my_incidents_by_country_trends": {
        "query": my_incidents_by_country_trends,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(d, "day", "count", "country"),
    },
    "my_incidents_by_source_trends": {
        "query": my_incidents_by_source_trends,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(d, "day", "count", "source"),
    },
    "incidents_by_action_trends": {
        "query": incidents_by_action_trends,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(d, "day", "count", "action"),
    },
    "port_trends": {
        "query": port_trends,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(d, "day", "count", "port"),
    },
    "top_passwords_popularity": {
        "query": top_passwords_popularity,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(
            d, "day", "count", "password"
        ),
    },
    "attacker_activity": {
        "query": attackers_activity_graph,
    },
    "password_in_time": {
        "query": password_activity_graph,
    },
    "password_logins": {
        "query": logins_of_password,
    },
}


PRECACHED_RESOURCES = [
    ("top_passwords", {"period": "1y"}),
    ("top_passwords_long", {"period": "1y"}),
    ("top_usernames", {"period": "1y"}),
    ("top_usernames_long", {"period": "1y"}),
    ("top_countries_by_attackers_table", {"period": "1y"}),
    ("top_countries_by_attackers_table_long", {"period": "1y"}),
    ("top_countries_by_incidents_table", {"period": "1y"}),
    ("top_countries_by_incidents_table_long", {"period": "1y"}),
    ("top_ips_long", {"period": "1y"}),
    ("top_combinations_long", {"period": "1y"}),
    ("attackers_map", {"period": "1y"}),
    ("incidents_map", {"period": "1y"}),
    ("attackers", {"period": "1y"}),
    ("attackers_trends", {"period": "1y"}),
    ("top_passwords_popularity", {"period": "1y"}),
]


def get_job_handler_key(resource_name, params):
    return "job_id:{}".format(
        ":".join(
            [resource_name]
            + [v for k, v in params.items() if k in KNOWN_PARAMS and v is not None]
        )
    )


def get_cached_data_key(resource_name, params):
    return "cached:{}".format(
        ":".join(
            [resource_name]
            + [v for k, v in params.items() if k in KNOWN_PARAMS and v is not None]
        )
    )
