# Graph of all scanned ports
all_ports_by_scans_graph = """
    SELECT
        to_char(bucket_inner, 'YYYY-MM-DD HH24:MI') as bucket,
        (CASE WHEN count_middle IS NULL THEN 0 ELSE count_middle END) AS count
    FROM (
        SELECT
            time_bucket(:bucket, time, to_timestamp(:start_ts)) AS bucket_inner,
            COUNT(*) as count_middle
        FROM ports
        WHERE
            to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
        GROUP BY bucket_inner
        ORDER BY bucket_inner
    ) as "raw_timing"
"""

# Graph of top ports by (number of) scans
top_ports_by_scans_graph = """
    SELECT
        to_char(bucket_inner, 'YYYY-MM-DD HH24:MI') as bucket,
        port,
        (CASE WHEN count_middle IS NULL THEN 0 ELSE count_middle END) AS count
    FROM (
        SELECT
            time_bucket(:bucket, time, to_timestamp(:start_ts)) AS bucket_inner,
            CONCAT(protocol, '/', port) AS port,
            COUNT(port) as count_middle
        FROM ports
        WHERE
            to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
            AND
            (port, protocol) IN (
                SELECT
                    port,
                    protocol
                FROM (
                    SELECT
                        port,
                        protocol,
                        COUNT(port) AS count_inner
                    FROM ports
                    WHERE
                        to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
                    GROUP BY port, protocol
                    ORDER BY count_inner DESC
                    LIMIT :limit
                ) AS foo
            )
        GROUP BY bucket_inner, port, protocol
        ORDER BY bucket_inner
    ) as "raw_timing"
"""

# Table of top ports by scans
top_ports_by_scans_list = """
    SELECT
        CONCAT(protocol, '/', port) AS port,
        COUNT(port) AS count
    FROM ports
    WHERE
        to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
    GROUP BY port, protocol
    ORDER BY count DESC
    LIMIT :limit
"""
