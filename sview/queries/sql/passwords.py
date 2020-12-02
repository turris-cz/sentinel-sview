top_passwords_popularity = """
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

password_activity_graph = """
    SELECT
        to_char(date_trunc('day', to_timestamp(ts)), 'YYYY-MM-DD') AS day,
        COUNT(*) as count
    FROM minipot_telnet
    WHERE
        password = :password
    GROUP BY day
    ORDER BY day
    """

logins_of_password = """
    SELECT
        username,
        COUNT(username) AS count
    FROM minipot_telnet
    WHERE
        password = :password
    GROUP BY username
    ORDER BY count DESC
    """

passwords_of_attacker = """
    SELECT
        password,
        count(password) AS count
    FROM minipot_telnet
    WHERE
        password IS NOT NULL
        AND
        password <> ''
        AND
        password <> '\n'
        AND
        ip = :ip
    GROUP BY password
    ORDER BY count DESC
    """
