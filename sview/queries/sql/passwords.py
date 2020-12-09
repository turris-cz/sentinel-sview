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
