from .post_process import as_map_data
from .post_process import as_multiline_graph_data

from .limits import limit_dashboard
from .limits import limit_long

from .flux.passwords import top_passwords
from .sql.passwords import top_usernames
from .sql.passwords import top_combinations
from .sql.passwords import top_passwords_popularity

from .sql.attackers import attackers_by_day
from .sql.attackers import attacker_ips

from .sql.countries import top_countries
from .sql.countries import map_overview
from .sql.countries import top_countries_trends


PRECACHED_QUERIES = {
    "top_passwords": {
        "query": top_passwords,
        "params": lambda: {"limit": limit_dashboard, "since": 0},
        "backend": "influx",
    },
    "top_passwords_long": {
        "query": top_passwords,
        "params": lambda: {"limit": limit_long, "since": 0},
        "backend": "influx",
    },
    "top_usernames": {
        "query": top_usernames,
        "params": lambda: {"limit": limit_dashboard, "since": 0},
    },
    "top_usernames_long": {
        "query": top_usernames,
        "params": lambda: {"limit": limit_long, "since": 0},
    },
    "top_countries": {
        "query": top_countries,
        "params": lambda: {"limit": limit_dashboard, "since": 0},
    },
    "top_countries_long": {
        "query": top_countries,
        "params": lambda: {"limit": limit_long, "since": 0},
    },
    "top_ips_long": {
        "query": attacker_ips,
        "params": lambda: {"limit": limit_long, "since": 0},
    },
    "top_combinations_long": {
        "query": top_combinations,
        "params": lambda: {"limit": limit_long, "since": 0},
    },
    "map_scores": {
        "query": map_overview,
        "params": lambda: {"since": 0},
        "post_process": lambda d: as_map_data(d, "country", "count"),
    },
    "attackers": {
        "query": attackers_by_day,
    },
    "attackers_trends": {
        "query": top_countries_trends,
        "params": {"top_n": limit_dashboard},
        "post_process": lambda d: as_multiline_graph_data(d, "day", "count", "country"),
    },
    "top_passwords_popularity": {
        "query": top_passwords_popularity,
        "params": {"top_n": limit_dashboard},
        "post_process": lambda d: as_multiline_graph_data(d, "day", "count", "password"),
    },
}
