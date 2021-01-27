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
    ("top_passwords",),
    ("top_passwords_long",),
    ("top_usernames",),
    ("top_usernames_long",),
    ("top_countries",),
    ("top_countries_long",),
    ("top_ips_long",),
    ("top_combinations_long",),
    ("map_scores",),
    ("attackers",),
    ("attackers_trends",),
    ("top_passwords_popularity",)
]
