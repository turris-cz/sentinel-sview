top_countries = """
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

map_overview = """
    SELECT
        country, count(country) AS count
    FROM minipot_telnet
    WHERE
        country IS NOT NULL
        AND
        ts > :since
    GROUP BY country
    """

top_countries_trends = """
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
