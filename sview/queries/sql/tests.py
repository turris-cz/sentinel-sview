_day_country_attackers = """
    SELECT
        country,
        count(country) as count
    FROM minipot_telnet
    WHERE
        to_char(date_trunc('day', to_timestamp(ts)), 'YYYY-MM-DD') = :day
        AND
        country IS NOT NULL
    GROUP BY country
    ORDER BY count DESC
    """

_day_ip_attackers = """
    SELECT
        ip,
        count(ip) as count
    FROM minipot_telnet
    WHERE
        to_char(date_trunc('day', to_timestamp(ts)), 'YYYY-MM-DD') = :day
        AND
        ip IS NOT NULL
    GROUP BY ip
    ORDER BY count DESC
    """
