from .post_process import as_map_data
from .post_process import as_multiline_graph_data

from .limits import limit_dashboard
from .limits import limit_long
from .limits import limit_plot

from .flux.passwords import top_passwords
from .flux.passwords import top_usernames
from .flux.passwords import top_combinations
from .flux.passwords import top_passwords_popularity

from .flux.attackers import attackers_by_day
from .flux.attackers import attacker_ips

from .flux.countries import top_countries
from .flux.countries import map_overview
from .flux.countries import top_countries_trends

PERIODS = {
    "1h": {
        "label": "Hour",
        "flux_start": "-1h",
        "flux_window": "1m",
    },
    "12h": {
        "label": "12 Hours",
        "flux_start": "-12h",
        "flux_window": "15m",
    },
    "1d": {
        "label": "Day",
        "flux_start": "-1d",
        "flux_window": "30m",
    },
    "1w": {
        "label": "Week",
        "flux_start": "-1w",
        "flux_window": "3h",
    },
    "1m": {
        "label": "Month",
        "flux_start": "-1mo",
        "flux_window": "1d",
    },
    "3m": {
        "label": "3 Months",
        "flux_start": "-3mo",
        "flux_window": "2d",
    },
    "1y": {
        "label": "Year",
        "flux_start": "-1y",
        "flux_window": "1w",
    },
}


RESOURCE_QUERIES = {
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
    "top_countries": {
        "query": top_countries,
        "params": {"limit": limit_dashboard},
    },
    "top_countries_long": {
        "query": top_countries,
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
    "map_scores": {
        "query": map_overview,
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
    "top_passwords_popularity": {
        "query": top_passwords_popularity,
        "params": {"top_n": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(d, "day", "count", "password"),
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
