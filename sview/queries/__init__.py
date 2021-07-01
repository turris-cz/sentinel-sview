from .post_process import as_map_data
from .post_process import as_multiline_graph_data

from .limits import limit_dashboard
from .limits import limit_long
from .limits import limit_plot

from .flux.passwords import top_passwords
from .flux.passwords import top_usernames
from .flux.passwords import top_combinations
from .flux.passwords import top_passwords_popularity
from .flux.passwords import password_activity_graph
from .flux.passwords import logins_of_password

from .flux.incidents import attackers_by_day
from .flux.incidents import attacker_ips
from .flux.incidents import attackers_activity_graph
from .flux.incidents import top_countries_by_incidents_table
from .flux.incidents import top_countries_by_attackers_table
from .flux.incidents import incidents_map
from .flux.incidents import attackers_map
from .flux.incidents import top_countries_trends
from .flux.incidents import all_incidents_graph
from .flux.incidents import my_incidents_graph
from .flux.incidents import top_incident_types
from .flux.incidents import incidents_by_country_trends
from .flux.incidents import incidents_by_source_trends
from .flux.incidents import incidents_by_action_trends

from .flux.ports import all_scans_graph
from .flux.ports import top_ports
from .flux.ports import port_trends

PERIODS = {
    "1h": {
        "label": "Hour",
        "flux_start": "-1h",
        "flux_window": "1m",
        "bucket": "sentinel-base",
    },
    "12h": {
        "label": "12 Hours",
        "flux_start": "-12h",
        "flux_window": "15m",
        "bucket": "sentinel-base",
    },
    "1d": {
        "label": "Day",
        "flux_start": "-1d",
        "flux_window": "30m",
        "bucket": "sentinel-base",
    },
    "1w": {
        "label": "Week",
        "flux_start": "-1w",
        "flux_window": "3h",
        "bucket": "sentinel-base",
    },
    "1m": {
        "label": "Month",
        "flux_start": "-1mo",
        "flux_window": "1d",
        "bucket": "sentinel-hourly",
    },
    "3m": {
        "label": "3 Months",
        "flux_start": "-3mo",
        "flux_window": "2d",
        "bucket": "sentinel-hourly",
    },
    "1y": {
        "label": "Year",
        "flux_start": "-1y",
        "flux_window": "1w",
        "bucket": "sentinel-daily",
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
        "params": {"top_n": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(d, "day", "count", "country"),
    },
    "incidents_by_country_trends": {
        "query": incidents_by_country_trends,
        "params": {"top_n": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(d, "day", "count", "country"),
    },
    "incidents_by_source_trends": {
        "query": incidents_by_source_trends,
        "params": {"top_n": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(d, "day", "count", "source"),
    },
    "incidents_by_action_trends": {
        "query": incidents_by_action_trends,
        "params": {"top_n": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(d, "day", "count", "action"),
    },
    "port_trends": {
        "query": port_trends,
        "params": {"top_n": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(d, "day", "count", "port"),
    },
    "top_passwords_popularity": {
        "query": top_passwords_popularity,
        "params": {"top_n": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(d, "day", "count", "password"),
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
    ("top_passwords", "1y"),
    ("top_passwords_long", "1y"),
    ("top_usernames", "1y"),
    ("top_usernames_long", "1y"),
    ("top_countries", "1y"),
    ("top_countries_long", "1y"),
    ("top_ips_long", "1y"),
    ("top_combinations_long", "1y"),
    ("map_scores", "1y"),
    ("attackers", "1y"),
    ("attackers_trends", "1y"),
    ("top_passwords_popularity", "1y")
]
