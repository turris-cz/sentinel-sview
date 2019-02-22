import datetime


def ts_today():
    d = datetime.datetime.utcnow()
    tr = datetime.datetime(d.year, d.month, d.day)
    return int(tr.timestamp())


def ts_this_week():
    d = datetime.datetime.utcnow()
    tr = datetime.datetime(d.year, d.month, d.day)
    tr = tr - datetime.timedelta(days=d.weekday())

    return int(tr.timestamp())


def ts_this_month():
    d = datetime.datetime.utcnow()
    tr = datetime.datetime(d.year, d.month, 1)

    return int(tr.timestamp())


def ts_this_year():
    d = datetime.datetime.utcnow()
    tr = datetime.datetime(d.year, 1, 1)

    return int(tr.timestamp())


def _as_multiline_graph_data(data, time_key, val_key, group_by):
    tmp = {}
    result = []
    groups = set()

    for i in data:
        if not i[time_key] in tmp:
            tmp[i[time_key]] = {}

        tmp[i[time_key]][i[group_by]] = i[val_key]
        groups.add(i[group_by])

    # Simply make one "official" order of the grouped variable for the rest of function
    groups = [g for g in groups]

    for key in sorted(tmp):
        item_dict = {
            time_key: key,
        }
        for i, g in enumerate(groups):
            item_dict[i] = tmp[key][g] if g in tmp[key] else 0
        result.append(item_dict)

    return {
        "labels": groups,
        "ykeys": [i for i in range(len(groups))],
        "data": result,
    }


def _as_map_data(data, key_key, val_key):
    return {i[key_key]: i[val_key] for i in data}


_passwords = """
    SELECT
        password, count(password) AS count
    FROM minipot_telnet
    WHERE
        password IS NOT NULL
        AND
        password <> ''
        AND
        password <> '\n'
        AND
        ts > :since
    GROUP BY password
    HAVING count(password) > 5
    ORDER BY count DESC
    LIMIT :limit
    """

_usernames = """
    SELECT
        username, count(username) AS count
    FROM minipot_telnet
    WHERE
        username IS NOT NULL
        AND
        username <> ''
        AND
        username <> '\n'
        AND
        ts > :since
    GROUP BY username
    HAVING count(username) > 5
    ORDER BY count DESC
    LIMIT :limit
    """

_countries = """
    SELECT
        country, count(country) AS count
    FROM minipot_telnet
    WHERE
        country IS NOT NULL
        AND
        ts > :since
    GROUP BY country
    HAVING count(country) > 5
    ORDER BY count DESC
    LIMIT :limit
    """

_combinations = """
    SELECT
        username, password, count(*) AS count
    FROM minipot_telnet
    WHERE
        username IS NOT NULL
        AND
        username <> ''
        AND
        username <> '\n'
        AND
        password IS NOT NULL
        AND
        password <> ''
        AND
        password <> '\n'
        AND
        ts > :since
    GROUP BY username, password
    HAVING count(*) > 5
    ORDER BY count DESC
    LIMIT :limit
    """

_map_scores = """
    SELECT
        country, count(country) AS count
    FROM minipot_telnet
    WHERE
        country IS NOT NULL
        AND
        ts > :since
    GROUP BY country
    """

_attackers = """
    SELECT
        to_char(date_trunc('day', to_timestamp(ts)), 'YYYY-MM-DD') AS day,
        COUNT(DISTINCT ip) as count
    FROM minipot_telnet
    WHERE
        action = 'login'
    GROUP BY day
    ORDER BY day
"""

_top_passwords_popularity = """
    SELECT
        to_char(date_trunc('day', to_timestamp(ts)), 'YYYY-MM-DD') AS day,
        password,
        COUNT(password) as count
    FROM minipot_telnet
    WHERE
        password IN (
            SELECT
                password
            FROM (
                SELECT
                    password,
                    COUNT(password) AS count_inner
                FROM minipot_telnet
                WHERE
                    password IS NOT NULL
                    AND
                    password <> ''
                    AND
                    password <> '\n'
                GROUP BY password
                ORDER BY count_inner DESC
                LIMIT :top_n
            ) AS foo
        )
    GROUP BY day, password
    ORDER BY day
"""

_top_countries_trends = """
    SELECT
        to_char(date_trunc('day', to_timestamp(ts)), 'YYYY-MM-DD') AS day,
        country,
        COUNT(DISTINCT ip) as count
    FROM minipot_telnet
    WHERE
        country IN (
            SELECT
                country
            FROM (
                SELECT
                    country,
                    COUNT(country) AS count_inner
                FROM minipot_telnet
                WHERE
                    country IS NOT NULL
                GROUP BY country
                ORDER BY count_inner DESC
                LIMIT :top_n
            ) AS foo
        )
    GROUP BY day, country
    ORDER BY day
"""

_limit_dashboard = 15
_limit_long = 30

QUERIES = {
    "top_passwords": {
        "query": _passwords,
        "params": lambda: {"limit": _limit_dashboard, "since": 0},
    },
    "top_passwords_long": {
        "query": _passwords,
        "params": lambda: {"limit": _limit_long, "since": 0},
    },
    "top_usernames": {
        "query": _usernames,
        "params": lambda: {"limit": _limit_dashboard, "since": 0},
    },
    "top_usernames_long": {
        "query": _usernames,
        "params": lambda: {"limit": _limit_long, "since": 0},
    },
    "top_countries": {
        "query": _countries,
        "params": lambda: {"limit": _limit_dashboard, "since": 0},
    },
    "top_countries_long": {
        "query": _countries,
        "params": lambda: {"limit": _limit_long, "since": 0},
    },
    "top_combinations_long": {
        "query": _combinations,
        "params": lambda: {"limit": _limit_long, "since": 0},
    },
    "map_scores": {
        "query": _map_scores,
        "params": lambda: {"since": 0},
        "post_process": lambda d: _as_map_data(d, "country", "count"),
    },
    "attackers": {
        "query": _attackers,
    },
    "attackers_trends": {
        "query": _top_countries_trends,
        "params": {"top_n": _limit_dashboard},
        "post_process": lambda d: _as_multiline_graph_data(d, "day", "count", "country"),
    },
    "top_passwords_popularity": {
        "query": _top_passwords_popularity,
        "params": {"top_n": _limit_dashboard},
        "post_process": lambda d: _as_multiline_graph_data(d, "day", "count", "password"),
    },
}
