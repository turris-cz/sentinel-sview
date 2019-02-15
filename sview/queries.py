QUERIES = {
    "top_passwords":
    """
    SELECT
        password, count(password) AS count
    FROM minipot_telnet
    WHERE
        password IS NOT NULL
    GROUP BY password
    HAVING count(password) > 5
    ORDER BY count DESC
    LIMIT 10
    """,


    "top_usernames":
    """
    SELECT
        username, count(username) AS count
    FROM minipot_telnet
    WHERE
        username IS NOT NULL
    GROUP BY username
    HAVING count(username) > 5
    ORDER BY count DESC
    LIMIT 10
    """,


    "top_countries":
    """
    SELECT
        country, count(country) AS count
    FROM minipot_telnet
    WHERE
        country IS NOT NULL
    GROUP BY country
    HAVING count(country) > 5
    ORDER BY count DESC
    LIMIT 10
    """,

    "top_combinations":
    """
    SELECT
        username, password, count(*) AS count
    FROM minipot_telnet
    WHERE
        username IS NOT NULL
        AND
        password IS NOT NULL
    GROUP BY username, password
    HAVING count(*) > 5
    ORDER BY count DESC
    LIMIT 20
    """,

    "map_scores":
    """
    SELECT
        country, count(country) AS count
    FROM minipot_telnet
    WHERE
        country IS NOT NULL
    GROUP BY country
    """,
}
