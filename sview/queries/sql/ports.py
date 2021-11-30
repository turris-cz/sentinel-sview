# Graph of all scanned ports
all_ports_by_scans_graph = """
    SELECT
        to_char((bucket_inner + INTERVAL :bucket) AT TIME ZONE 'UTC', 'YYYY-MM-DD HH24:MI') as bucket,
        (CASE WHEN count_middle IS NULL THEN 0 ELSE count_middle END) AS count
    FROM (
        SELECT
            time_bucket(:bucket, time, to_timestamp(:start_ts)) AS bucket_inner,
            SUM(raw_count) as count_middle
        FROM {source_table}
        WHERE
            to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
        GROUP BY bucket_inner
        ORDER BY bucket_inner
    ) as "raw_timing"
"""

# Graph of top ports by (number of) scans
top_ports_by_scans_graph = """
    SELECT
        to_char((bucket_inner + INTERVAL :bucket) AT TIME ZONE 'UTC', 'YYYY-MM-DD HH24:MI') as bucket,
        port,
        (CASE WHEN count_middle IS NULL THEN 0 ELSE count_middle END) AS count
    FROM (
        SELECT
            time_bucket(:bucket, time, to_timestamp(:start_ts)) AS bucket_inner,
            CONCAT(protocol, '/', port) AS port,
            SUM(raw_count) as count_middle
        FROM {source_table}
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
                        SUM(raw_count) AS count_inner
                    FROM {source_table}
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
        SUM(raw_count) AS count
    FROM {source_table}
    WHERE
        to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
    GROUP BY port, protocol
    ORDER BY count DESC
    LIMIT :limit
"""
