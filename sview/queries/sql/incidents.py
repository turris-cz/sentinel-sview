# Graph of all incidents
all_incidents_graph = """
    SELECT
        to_char((bucket_inner + INTERVAL :bucket) AT TIME ZONE 'UTC', 'YYYY-MM-DD HH24:MI') as bucket,
        (CASE WHEN count_middle IS NULL THEN 0 ELSE count_middle END) AS count
    FROM (
        SELECT
            time_bucket(:bucket, time, to_timestamp(:start_ts)) AS bucket_inner,
            SUM(raw_count) as count_middle
        FROM incidents
        WHERE
            to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
        GROUP BY bucket_inner
        ORDER BY bucket_inner
    ) as "raw_timing"
"""

# List of top incident types by incidents
top_incident_types_by_incidents_list = """
    SELECT
        SUM(raw_count) as count,
        trap as source,
        action
    FROM incidents
    WHERE
        to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
    GROUP BY trap, action
    ORDER BY count DESC
    LIMIT :limit
"""

# Graph of top traps by incidents
top_traps_by_incidents_graph = """
    SELECT
        to_char((bucket_inner + INTERVAL :bucket) AT TIME ZONE 'UTC', 'YYYY-MM-DD HH24:MI') as bucket,
        source,
        (CASE WHEN count_middle IS NULL THEN 0 ELSE count_middle END) AS count
    FROM (
        SELECT
            time_bucket(:bucket, time, to_timestamp(:start_ts)) AS bucket_inner,
            trap as source,
            SUM(raw_count) as count_middle
        FROM incidents
        WHERE
            trap IN (
                SELECT
                    trap
                FROM (
                    SELECT
                        trap,
                        SUM(raw_count) AS count_inner
                    FROM incidents
                    WHERE
                        trap IS NOT NULL
                        AND
                        to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
                    GROUP BY trap
                    ORDER BY count_inner DESC
                    LIMIT :limit
                ) AS foo
            )
            AND
            to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
        GROUP BY bucket_inner, trap
        ORDER BY bucket_inner
    ) as "raw_timing"
"""

# Graph of top actions by incidents
top_actions_by_incidents_graph = """
    SELECT
        to_char((bucket_inner + INTERVAL :bucket) AT TIME ZONE 'UTC', 'YYYY-MM-DD HH24:MI') as bucket,
        action,
        (CASE WHEN count_middle IS NULL THEN 0 ELSE count_middle END) AS count
    FROM (
        SELECT
            time_bucket(:bucket, time, to_timestamp(:start_ts)) AS bucket_inner,
            action,
            SUM(raw_count) as count_middle
        FROM incidents
        WHERE
            action IN (
                SELECT
                    action
                FROM (
                    SELECT
                        action,
                        SUM(raw_count) AS count_inner
                    FROM incidents
                    WHERE
                        action IS NOT NULL
                        AND
                        to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
                    GROUP BY action
                    ORDER BY count_inner DESC
                    LIMIT :limit
                ) AS foo
            )
            AND
            to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
        GROUP BY bucket_inner, action
        ORDER BY bucket_inner
    ) as "raw_timing"
"""

# List of top attackers by incidents
top_attackers_by_incidents_list = """
    SELECT
        ip,
        SUM(raw_count) AS count
    FROM incidents
    WHERE
        ip IS NOT NULL
        AND
        to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
    GROUP BY ip
    ORDER BY count DESC
    LIMIT :limit
"""

# Graph of all attackers
all_attackers_graph = """
    SELECT
        to_char((bucket_inner + INTERVAL :bucket) AT TIME ZONE 'UTC', 'YYYY-MM-DD HH24:MI') as bucket,
        (CASE WHEN count_middle IS NULL THEN 0 ELSE count_middle END) AS count
    FROM (
        SELECT
            time_bucket(:bucket, time, to_timestamp(:start_ts)) AS bucket_inner,
            COUNT(DISTINCT ip) as count_middle
        FROM incidents
        WHERE
            to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
        GROUP BY bucket_inner
        ORDER BY bucket_inner
    ) as "raw_timing"
"""

# Graph of selected attacker's incidents
selected_attacker_incidents_graph = """
    SELECT
        to_char((bucket_inner + INTERVAL :bucket) AT TIME ZONE 'UTC', 'YYYY-MM-DD HH24:MI') as bucket,
        (CASE WHEN count_middle IS NULL THEN 0 ELSE count_middle END) AS count
    FROM (
        SELECT
            time_bucket(:bucket, time, to_timestamp(:start_ts)) AS bucket_inner,
            SUM(raw_count) as count_middle
        FROM incidents
        WHERE
            ip = :ip
            AND
            to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
        GROUP BY bucket_inner
        ORDER BY bucket_inner
    ) as "raw_timing"
"""

# List of top countries by incidents
top_countries_by_incidents_list = """
    SELECT
        country,
        SUM(raw_count) AS count
    FROM incidents
    WHERE
        country IS NOT NULL
        AND
        to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
    GROUP BY country
    ORDER BY count DESC
    LIMIT :limit
"""

# List of top countries by attackers
top_countries_by_attackers_list = """
    SELECT
        country,
        COUNT(distinct(ip)) AS count
    FROM incidents
    WHERE
        ip IS NOT NULL
        AND
        to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
    GROUP BY country
    ORDER BY count DESC
    LIMIT :limit
"""

# List of all countries by incidents
all_countries_by_incidents_list = """
    SELECT
        country,
        SUM(raw_count) AS count
    FROM incidents
    WHERE
        country IS NOT NULL
        AND
        to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
    GROUP BY country
"""

# List of all countries by attackers
all_countries_by_attackers_list = """
    SELECT
        country,
        COUNT(distinct(ip)) AS count
    FROM incidents
    WHERE
        country IS NOT NULL
        AND
        to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
        AND
        ip is not null
    GROUP BY country
"""

# Graph of top countries by attackers
top_countries_by_attackers_graph = """
    SELECT
        to_char((bucket_inner + INTERVAL :bucket) AT TIME ZONE 'UTC', 'YYYY-MM-DD HH24:MI') as bucket,
        country,
        (CASE WHEN count_middle IS NULL THEN 0 ELSE count_middle END) AS count
    FROM (
        SELECT
            time_bucket(:bucket, time, to_timestamp(:start_ts)) AS bucket_inner,
            country,
            COUNT(DISTINCT ip) as count_middle
        FROM incidents
        WHERE
            to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
            AND country IN (
                SELECT
                    country
                FROM (
                    SELECT
                        country,
                        COUNT(DISTINCT(ip)) AS count_inner
                    FROM incidents
                    WHERE
                        to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
                        AND
                        country IS NOT NULL
                    GROUP BY country
                    ORDER BY count_inner DESC
                    LIMIT :limit
                ) AS foo
            )
        GROUP BY bucket_inner, country
        ORDER BY bucket_inner
    ) as "raw_timing"
"""

# Graph of top countries by incidents
top_countries_by_incidents_graph = """
    SELECT
        to_char((bucket_inner + INTERVAL :bucket) AT TIME ZONE 'UTC', 'YYYY-MM-DD HH24:MI') as bucket,
        country,
        (CASE WHEN count_middle IS NULL THEN 0 ELSE count_middle END) AS count
    FROM (
        SELECT
            time_bucket(:bucket, time, to_timestamp(:start_ts)) AS bucket_inner,
            country,
            SUM(raw_count) as count_middle
        FROM incidents
        WHERE
            to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
            AND
            country IN (
                SELECT
                    country
                FROM (
                    SELECT
                        country,
                        SUM(raw_count) AS count_inner
                    FROM incidents
                    WHERE
                        to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
                        AND
                        country IS NOT NULL
                    GROUP BY country
                    ORDER BY count_inner DESC
                    LIMIT :limit
                ) AS foo
            )
        GROUP BY bucket_inner, country
        ORDER BY bucket_inner
    ) as "raw_timing"
"""

# Graph of top countries by incidents reported by selected devices
my_top_countries_by_incidents_graph = """
    SELECT
        to_char((bucket_inner + INTERVAL :bucket) AT TIME ZONE 'UTC', 'YYYY-MM-DD HH24:MI') as bucket,
        country,
        (CASE WHEN count_middle IS NULL THEN 0 ELSE count_middle END) AS count
    FROM (
        SELECT
            time_bucket(:bucket, time, to_timestamp(:start_ts)) AS bucket_inner,
            incidents.country AS country,
            SUM(incidents.raw_count) as count_middle
        FROM incidents, identity
        WHERE
            to_timestamp(:start_ts) <= incidents.time AND incidents.time < to_timestamp(:finish_ts)
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
                        SUM(incidents.raw_count) AS count_inner
                    FROM incidents, identity
                    WHERE
                        to_timestamp(:start_ts) <= incidents.time AND incidents.time < to_timestamp(:finish_ts)
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
        GROUP BY bucket_inner, country
        ORDER BY bucket_inner
    ) as "raw_timing"
"""

# Graph of top traps by incidents reported by selected devices
my_top_traps_by_incidents_graph = """
    SELECT
        to_char((bucket_inner + INTERVAL :bucket) AT TIME ZONE 'UTC', 'YYYY-MM-DD HH24:MI') as bucket,
        source,
        (CASE WHEN count_middle IS NULL THEN 0 ELSE count_middle END) AS count
    FROM (
        SELECT
            time_bucket(:bucket, time, to_timestamp(:start_ts)) AS bucket_inner,
            incidents.trap AS source,
            SUM(incidents.raw_count) as count_middle
        FROM incidents, identity
        WHERE
            to_timestamp(:start_ts) <= incidents.time AND incidents.time < to_timestamp(:finish_ts)
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
                        SUM(incidents.raw_count) AS count_inner
                    FROM incidents, identity
                    WHERE
                        to_timestamp(:start_ts) <= incidents.time AND incidents.time < to_timestamp(:finish_ts)
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
        GROUP BY bucket_inner, source
        ORDER BY bucket_inner
    ) as "raw_timing"
"""

# Graph of all incidents reported by selected devices
my_all_incidents_graph = """
    SELECT
        to_char((bucket_inner + INTERVAL :bucket) AT TIME ZONE 'UTC', 'YYYY-MM-DD HH24:MI') as bucket,
        (CASE WHEN count_middle IS NULL THEN 0 ELSE count_middle END) AS count
    FROM (
        SELECT
            time_bucket(:bucket, time, to_timestamp(:start_ts)) AS bucket_inner,
            SUM(incidents.raw_count) as count_middle
        FROM incidents, identity
        WHERE
            to_timestamp(:start_ts) <= incidents.time AND incidents.time < to_timestamp(:finish_ts)
            AND
            incidents.identity_id=identity.id
            AND
            identity.device_token in :my_device_tokens
        GROUP BY bucket_inner
        ORDER BY bucket_inner
    ) as "raw_timing"
"""
