# Graph of all scanned ports
all_ports_by_scans_graph = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS bucket,
        COUNT(*) as count
    FROM ports
    WHERE
        now() - INTERVAL :interval < time AND time < now()
    GROUP BY bucket
    ORDER BY bucket
"""

# Graph of top ports by (number of) scans
top_ports_by_scans_graph = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS bucket,
        CONCAT(protocol, '/', port) AS port,
        COUNT(port) as count
    FROM ports
    WHERE
        now() - INTERVAL :interval < time AND time < now()
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
                    now() - INTERVAL :interval < time AND time < now()
                GROUP BY port, protocol
                ORDER BY count_inner DESC
                LIMIT :limit
            ) AS foo
        )
    GROUP BY bucket, port, protocol
    ORDER BY bucket
"""

# Table of top ports by scans
top_ports_by_scans_list = """
    SELECT
        CONCAT(protocol, '/', port) AS port,
        COUNT(port) AS count
    FROM ports
    WHERE
        now() - INTERVAL :interval < time AND time < now()
    GROUP BY port, protocol
    ORDER BY count DESC
    LIMIT :limit
"""
