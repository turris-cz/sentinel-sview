# Graph of all incidents
all_incidents_graph = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS bucket,
        COUNT(*) as count
    FROM incidents
    WHERE
        now() - INTERVAL :interval < time AND time < now()
    GROUP BY bucket
    ORDER BY bucket
"""

# List of top incident types by incidents
top_incident_types_by_incidents_list = """
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
top_traps_by_incidents_graph = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS bucket,
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
    GROUP BY bucket, trap
    ORDER BY bucket
"""

# Graph of top actions by incidents
top_actions_by_incidents_graph = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS bucket,
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
    GROUP BY bucket, action
    ORDER BY bucket
"""

# List of top attackers by incidents
top_attackers_by_incidents_list = """
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
all_attackers_graph = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS bucket,
        COUNT(DISTINCT ip) as count
    FROM incidents
    WHERE
        now() - INTERVAL :interval < time AND time < now()
    GROUP BY bucket
    ORDER BY bucket
"""

# Graph of selected attacker's incidents
selected_attacker_incidents_graph = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS bucket,
        COUNT(*) as count
    FROM incidents
    WHERE
        ip = :ip
        AND
        now() - INTERVAL :interval < time AND time < now()
    GROUP BY bucket
    ORDER BY bucket
"""

# List of top countries by incidents
top_countries_by_incidents_list = """
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
top_countries_by_attackers_list = """
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
all_countries_by_incidents_list = """
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
all_countries_by_attackers_list = """
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
top_countries_by_attackers_graph = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS bucket,
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
    GROUP BY bucket, country
    ORDER BY bucket
"""

# Graph of top countries by incidents
top_countries_by_incidents_graph = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS bucket,
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
    GROUP BY bucket, country
    ORDER BY bucket
"""

# Graph of top countries by incidents reported by selected devices
my_top_countries_by_incidents_graph = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS bucket,
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
    GROUP BY bucket, country
    ORDER BY bucket
"""

# Graph of top traps by incidents reported by selected devices
my_top_traps_by_incidents_graph = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS bucket,
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
    GROUP BY bucket, source
    ORDER BY bucket
"""

# Graph of all incidents reported by selected devices
my_all_incidents_graph = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS bucket,
        COUNT(*) as count
    FROM incidents, identity
    WHERE
        now() - INTERVAL :interval < incidents.time AND incidents.time < now()
        AND
        incidents.identity_id=identity.id
        AND
        identity.device_token in :my_device_tokens
    GROUP BY bucket
    ORDER BY bucket
"""
