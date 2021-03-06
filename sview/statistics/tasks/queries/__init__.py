from .post_process import as_map_data
from .post_process import as_multiline_graph_data

from .limits import limit_dashboard
from .limits import limit_long
from .limits import limit_plot

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


class DataTypes:
    PORTS = "ports"
    INCIDENTS = "incidents"
    PASSWORDS = "passwords"


KNOWN_PARAMS = {
    "period": "1y",
    "ip": None,
    "password": None,
    "token": None,
}


RESOURCE_QUERIES = {
    "all_incidents_graph": {
        "query": all_incidents_graph,
        "data_type": DataTypes.INCIDENTS,
    },
    "my_all_incidents_graph": {
        "query": my_all_incidents_graph,
        "data_type": DataTypes.INCIDENTS,
    },
    "all_ports_by_scans_graph": {
        "query": all_ports_by_scans_graph,
        "data_type": DataTypes.PORTS,
    },
    "top_passwords_by_usages_list": {
        "query": top_passwords_by_usages_list,
        "params": {"limit": limit_dashboard},
        "data_type": DataTypes.PASSWORDS,
    },
    "top_passwords_by_usages_list_long": {
        "query": top_passwords_by_usages_list,
        "params": {"limit": limit_long},
        "data_type": DataTypes.PASSWORDS,
    },
    "top_usernames_by_usages_list": {
        "query": top_usernames_by_usages_list,
        "params": {"limit": limit_dashboard},
        "data_type": DataTypes.PASSWORDS,
    },
    "top_usernames_by_usages_list_long": {
        "query": top_usernames_by_usages_list,
        "params": {"limit": limit_long},
        "data_type": DataTypes.PASSWORDS,
    },
    "top_ports_by_scans_list_long": {
        "query": top_ports_by_scans_list,
        "params": {"limit": limit_long},
        "data_type": DataTypes.PORTS,
    },
    "top_countries_by_incidents_list": {
        "query": top_countries_by_incidents_list,
        "params": {"limit": limit_dashboard},
        "data_type": DataTypes.INCIDENTS,
    },
    "top_countries_by_incidents_list_long": {
        "query": top_countries_by_incidents_list,
        "params": {"limit": limit_long},
        "data_type": DataTypes.INCIDENTS,
    },
    "top_countries_by_attackers_list": {
        "query": top_countries_by_attackers_list,
        "params": {"limit": limit_dashboard},
        "data_type": DataTypes.INCIDENTS,
    },
    "top_countries_by_attackers_list_long": {
        "query": top_countries_by_attackers_list,
        "params": {"limit": limit_long},
        "data_type": DataTypes.INCIDENTS,
    },
    "top_attackers_by_incidents_list_long": {
        "query": top_attackers_by_incidents_list,
        "params": {"limit": limit_long},
        "data_type": DataTypes.INCIDENTS,
    },
    "top_combinations_by_usages_list_long": {
        "query": top_combinations_by_usages_list,
        "params": {"limit": limit_long},
        "data_type": DataTypes.PASSWORDS,
    },
    "top_incident_types_by_incidents_list": {
        "query": top_incident_types_by_incidents_list,
        "params": {"limit": limit_dashboard},
        "data_type": DataTypes.INCIDENTS,
    },
    "all_countries_by_incidents_list": {
        "query": all_countries_by_incidents_list,
        "post_process": lambda d: as_map_data(d, "country", "count"),
        "data_type": DataTypes.INCIDENTS,
    },
    "all_countries_by_attackers_list": {
        "query": all_countries_by_attackers_list,
        "post_process": lambda d: as_map_data(d, "country", "count"),
        "data_type": DataTypes.INCIDENTS,
    },
    "all_attackers_graph": {
        "query": all_attackers_graph,
        "data_type": DataTypes.INCIDENTS,
    },
    "top_countries_by_attackers_graph": {
        "query": top_countries_by_attackers_graph,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(
            d, "bucket", "count", "country"
        ),
        "data_type": DataTypes.INCIDENTS,
    },
    "top_countries_by_incidents_graph": {
        "query": top_countries_by_incidents_graph,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(
            d, "bucket", "count", "country"
        ),
        "data_type": DataTypes.INCIDENTS,
    },
    "top_traps_by_incidents_graph": {
        "query": top_traps_by_incidents_graph,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(
            d, "bucket", "count", "source"
        ),
        "data_type": DataTypes.INCIDENTS,
    },
    "my_top_countries_by_incidents_graph": {
        "query": my_top_countries_by_incidents_graph,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(
            d, "bucket", "count", "country"
        ),
        "empty_response": {"data": []},
        "data_type": DataTypes.INCIDENTS,
    },
    "my_top_traps_by_incidents_graph": {
        "query": my_top_traps_by_incidents_graph,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(
            d, "bucket", "count", "source"
        ),
        "empty_response": {"data": []},
        "data_type": DataTypes.INCIDENTS,
    },
    "top_actions_by_incidents_graph": {
        "query": top_actions_by_incidents_graph,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(
            d, "bucket", "count", "action"
        ),
        "data_type": DataTypes.INCIDENTS,
    },
    "top_ports_by_scans_graph": {
        "query": top_ports_by_scans_graph,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(d, "bucket", "count", "port"),
        "data_type": DataTypes.PORTS,
    },
    "top_passwords_by_usages_graph": {
        "query": top_passwords_by_usages_graph,
        "params": {"limit": limit_plot},
        "post_process": lambda d: as_multiline_graph_data(
            d, "bucket", "count", "password"
        ),
        "data_type": DataTypes.PASSWORDS,
    },
    "selected_attacker_incidents_graph": {
        "query": selected_attacker_incidents_graph,
        "data_type": DataTypes.INCIDENTS,
    },
    "selected_password_by_usages_graph": {
        "query": selected_password_by_usages_graph,
        "data_type": DataTypes.PASSWORDS,
    },
    "logins_of_password_by_usages_list": {
        "query": logins_of_password_by_usages_list,
        "params": {"limit": limit_long},
        "data_type": DataTypes.PASSWORDS,
    },
}


PRECACHED_RESOURCES = [
    "all_incidents_graph",
    "all_ports_by_scans_graph",
    "top_passwords_by_usages_list",
    "top_passwords_by_usages_list_long",
    "top_usernames_by_usages_list",
    "top_usernames_by_usages_list_long",
    "top_ports_by_scans_list_long",
    "top_countries_by_incidents_list",
    "top_countries_by_incidents_list_long",
    "top_countries_by_attackers_list",
    "top_countries_by_attackers_list_long",
    "top_attackers_by_incidents_list_long",
    "top_combinations_by_usages_list_long",
    "top_incident_types_by_incidents_list",
    "all_countries_by_incidents_list",
    "all_countries_by_attackers_list",
    "all_attackers_graph",
    "top_countries_by_attackers_graph",
    "top_countries_by_incidents_graph",
    "top_traps_by_incidents_graph",
    "top_actions_by_incidents_graph",
    "top_ports_by_scans_graph",
    "top_passwords_by_usages_graph",
]
