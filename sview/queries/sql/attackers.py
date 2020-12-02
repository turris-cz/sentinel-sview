attackers_activity_graph = """
    SELECT
        to_char(date_trunc('day', to_timestamp(ts)), 'YYYY-MM-DD') AS day,
        COUNT(*) as count
    FROM minipot_telnet
    WHERE
        ip = :ip
    GROUP BY day
    ORDER BY day
    """

attackers_of_password = """
    SELECT
        ip,
        COUNT(ip) AS count
    FROM minipot_telnet
    WHERE
        password = :password
    GROUP BY ip
    HAVING COUNT(ip) > 5
    ORDER BY count DESC
    """
