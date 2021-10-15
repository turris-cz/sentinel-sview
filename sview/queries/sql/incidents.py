# Graph of all incidents
all_incidents_graph = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS day,
        COUNT(*) as count
    FROM incidents
    WHERE
        now() - INTERVAL :interval < time AND time < now()
    GROUP BY day
    ORDER BY day
"""

# List of top incident types by incidents
top_incident_types = """
    SELECT
        count(*) as count,
        trap as source,
        action
    FROM incidents
    WHERE
        now() - INTERVAL :interval < time AND time < now()
    GROUP BY trap, action
    ORDER BY count DESC
    LIMIT :limit
"""

# Graph of top traps by incidents
incidents_by_source_trends = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS day,
        trap as source,
        COUNT(ip) as count
    FROM incidents
    WHERE
        trap IN (
            SELECT
                trap
            FROM (
                SELECT
                    trap,
                    COUNT(*) AS count_inner
                FROM incidents
                WHERE
                    trap IS NOT NULL
                    AND
                    now() - INTERVAL :interval < time AND time < now()
                GROUP BY trap
                ORDER BY count_inner DESC
                LIMIT :limit
            ) AS foo
        )
        AND
        now() - INTERVAL :interval < time AND time < now()
    GROUP BY day, trap
    ORDER BY day
"""

# Graph of top actions by incidents
incidents_by_action_trends = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS day,
        action,
        COUNT(ip) as count
    FROM incidents
    WHERE
        action IN (
            SELECT
                action
            FROM (
                SELECT
                    action,
                    COUNT(*) AS count_inner
                FROM incidents
                WHERE
                    action IS NOT NULL
                    AND
                    now() - INTERVAL :interval < time AND time < now()
                GROUP BY action
                ORDER BY count_inner DESC
                LIMIT :limit
            ) AS foo
        )
        AND
        now() - INTERVAL :interval < time AND time < now()
    GROUP BY day, action
    ORDER BY day
"""

# List of top attackers by incidents
attacker_ips = """
    SELECT
        ip,
        count(ip) AS count
    FROM incidents
    WHERE
        ip IS NOT NULL
        AND
        now() - INTERVAL :interval < time AND time < now()
    GROUP BY ip
    ORDER BY count DESC
    LIMIT :limit
"""

# Graph of all attackers
attackers_by_day = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS day,
        COUNT(DISTINCT ip) as count
    FROM incidents
    WHERE
        now() - INTERVAL :interval < time AND time < now()
    GROUP BY day
    ORDER BY day
"""

# Graph of selected attacker's incidents
attackers_activity_graph = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS day,
        COUNT(*) as count
    FROM incidents
    WHERE
        ip = :ip
        AND
        now() - INTERVAL :interval < time AND time < now()
    GROUP BY day
    ORDER BY day
"""

# List of top countries by incidents
top_countries_by_incidents_table = """
    SELECT
        country,
        count(country) AS count
    FROM incidents
    WHERE
        country IS NOT NULL
        AND
        now() - INTERVAL :interval < time AND time < now()
    GROUP BY country
    ORDER BY count DESC
    LIMIT :limit
"""

# List of top countries by attackers
top_countries_by_attackers_table = """
    SELECT
        country,
        count(distinct(ip)) AS count
    FROM incidents
    WHERE
        ip IS NOT NULL
        AND
        now() - INTERVAL :interval < time AND time < now()
    GROUP BY country
    ORDER BY count DESC
    LIMIT :limit
"""

# List of all countries by incidents
incidents_map = """
    SELECT
        country,
        count(*) AS count
    FROM incidents
    WHERE
        country IS NOT NULL
        AND
        now() - INTERVAL :interval < time AND time < now()
    GROUP BY country
"""

# List of all countries by attackers
attackers_map = """
    SELECT
        country,
        count(distinct(ip)) AS count
    FROM incidents
    WHERE
        country IS NOT NULL
        AND
        now() - INTERVAL :interval < time AND time < now()
        AND
        ip is not null
    GROUP BY country
"""

# Graph of top countries by attackers
top_countries_trends = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS day,
        country,
        COUNT(DISTINCT ip) as count
    FROM incidents
    WHERE
        now() - INTERVAL :interval < time AND time < now()
        AND country IN (
            SELECT
                country
            FROM (
                SELECT
                    country,
                    COUNT(DISTINCT(ip)) AS count_inner
                FROM incidents
                WHERE
                    now() - INTERVAL :interval < time AND time < now()
                    AND
                    country IS NOT NULL
                GROUP BY country
                ORDER BY count_inner DESC
                LIMIT :limit
            ) AS foo
        )
    GROUP BY day, country
    ORDER BY day
"""

# Graph of top countries by incidents
incidents_by_country_trends = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS day,
        country,
        COUNT(*) as count
    FROM incidents
    WHERE
        now() - INTERVAL :interval < time AND time < now()
        AND
        country IN (
            SELECT
                country
            FROM (
                SELECT
                    country,
                    COUNT(*) AS count_inner
                FROM incidents
                WHERE
                    now() - INTERVAL :interval < time AND time < now()
                    AND
                    country IS NOT NULL
                GROUP BY country
                ORDER BY count_inner DESC
                LIMIT :limit
            ) AS foo
        )
    GROUP BY day, country
    ORDER BY day
"""

# Graph of top countries by incidents reported by selected devices
my_incidents_by_country_trends = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS day,
        incidents.country AS country,
        COUNT(*) as count
    FROM incidents, identity
    WHERE
        now() - INTERVAL :interval < incidents.time AND incidents.time < now()
        AND
        identity.device_token in :my_device_tokens
        AND
        incidents.identity_id=identity.id
        AND
        incidents.country IN (
            SELECT
                country_inner
            FROM (
                SELECT
                    incidents.country as country_inner,
                    COUNT(*) AS count_inner
                FROM incidents, identity
                WHERE
                    now() - INTERVAL :interval < incidents.time AND incidents.time < now()
                    AND
                    incidents.country IS NOT NULL
                    AND
                    incidents.identity_id=identity.id
                    AND
                    identity.device_token in :my_device_tokens
                GROUP BY country_inner
                ORDER BY count_inner DESC
                LIMIT :limit
            ) AS top_countries
        )
    GROUP BY day, country
    ORDER BY day
"""

# Graph of top traps by incidents reported by selected devices
my_incidents_by_source_trends = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS day,
        incidents.trap AS source,
        COUNT(*) as count
    FROM incidents, identity
    WHERE
        now() - INTERVAL :interval < incidents.time AND incidents.time < now()
        AND
        identity.device_token in :my_device_tokens
        AND
        incidents.identity_id=identity.id
        AND
        incidents.trap IN (
            SELECT
                trap_inner
            FROM (
                SELECT
                    incidents.trap as trap_inner,
                    COUNT(*) AS count_inner
                FROM incidents, identity
                WHERE
                    now() - INTERVAL :interval < incidents.time AND incidents.time < now()
                    AND
                    incidents.trap IS NOT NULL
                    AND
                    incidents.identity_id=identity.id
                    AND
                    identity.device_token in :my_device_tokens
                GROUP BY trap_inner
                ORDER BY count_inner DESC
                LIMIT :limit
            ) AS top_traps
        )
    GROUP BY day, source
    ORDER BY day
"""

# Graph of all incidents reported by selected devices
my_incidents_graph = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS day,
        COUNT(*) as count
    FROM incidents, identity
    WHERE
        now() - INTERVAL :interval < incidents.time AND incidents.time < now()
        AND
        incidents.identity_id=identity.id
        AND
        identity.device_token in :my_device_tokens
    GROUP BY day
    ORDER BY day
"""
