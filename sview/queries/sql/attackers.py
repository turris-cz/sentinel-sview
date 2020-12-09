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
