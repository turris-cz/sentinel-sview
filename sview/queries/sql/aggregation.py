aggregation_queries = {
    "incidents": """
        INSERT INTO
            {destination_table} (time, raw_count, identity_id, trap, action, ip, country)
        SELECT
            time_bucket(:bucket, time, to_timestamp(:start_ts)) AS bucket_inner,
            SUM(raw_count),
            identity_id,
            trap,
            action,
            ip,
            country
        FROM {source_table}
        WHERE
            to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
        GROUP BY bucket_inner, identity_id, trap, action, ip, country
        ORDER BY bucket_inner
    """,
    "passwords": """
        INSERT INTO
            {destination_table} (time, raw_count, username, password)
        SELECT
            time_bucket(:bucket, time, to_timestamp(:start_ts)) AS bucket_inner,
            SUM(raw_count),
            username,
            password
        FROM {source_table}
        WHERE
            to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
        GROUP BY bucket_inner, username, password
        ORDER BY bucket_inner
    """,
    "ports": """
        INSERT INTO
            {destination_table} (time, raw_count, port, protocol)
        SELECT
            time_bucket(:bucket, time, to_timestamp(:start_ts)) AS bucket_inner,
            SUM(raw_count),
            port,
            protocol
        FROM {source_table}
        WHERE
            to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
        GROUP BY bucket_inner, port, protocol
        ORDER BY bucket_inner
    """,
}
