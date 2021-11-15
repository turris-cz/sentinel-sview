# List of top passwords by ussages
top_passwords_by_usages_list = """
    SELECT
        password,
        count(*) AS count
    FROM passwords
    WHERE
        password IS NOT NULL
        AND
        password <> ''
        AND
        password <> '\n'
        AND
        to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
    GROUP BY password
    ORDER BY count DESC
    LIMIT :limit
"""

# List of top usernames by ussages
top_usernames_by_usages_list = """
    SELECT
        username,
        count(*) AS count
    FROM passwords
    WHERE
        username IS NOT NULL
        AND
        username <> ''
        AND
        username <> '\n'
        AND
        to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
    GROUP BY username
    ORDER BY count DESC
    LIMIT :limit
"""

# List of top combinations by ussages
top_combinations_by_usages_list = """
    SELECT
        username,
        password,
        count(*) AS count
    FROM passwords
    WHERE
        username IS NOT NULL
        AND
        username <> ''
        AND
        username <> '\n'
        AND
        password IS NOT NULL
        AND
        password <> ''
        AND
        password <> '\n'
        AND
        to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
    GROUP BY username, password
    ORDER BY count DESC
    LIMIT :limit
"""

# Graph of top passwords by ussages
top_passwords_by_usages_graph = """
    SELECT
        to_char(bucket_inner, 'YYYY-MM-DD HH24:MI') as bucket,
        password,
        (CASE WHEN count_middle IS NULL THEN 0 ELSE count_middle END) AS count
    FROM (
        SELECT
            time_bucket(:bucket, time, to_timestamp(:start_ts)) AS bucket_inner,
            password,
            COUNT(*) as count_middle
        FROM passwords
        WHERE
            password IN (
                SELECT
                    password
                FROM (
                    SELECT
                        password,
                        COUNT(*) AS count_inner
                    FROM passwords
                    WHERE
                        password IS NOT NULL
                        AND
                        password <> ''
                        AND
                        password <> '\n'
                        AND
                        to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
                    GROUP BY password
                    ORDER BY count_inner DESC
                    LIMIT :limit
                ) AS foo
            )
            AND
            to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
        GROUP BY bucket_inner, password
        ORDER BY bucket_inner
    ) as "raw_timing"
"""

# Graph of selected passwords's ussages
selected_password_by_usages_graph = """
    SELECT
        to_char(bucket_inner, 'YYYY-MM-DD HH24:MI') as bucket,
        (CASE WHEN count_middle IS NULL THEN 0 ELSE count_middle END) AS count
    FROM (
        SELECT
            time_bucket(:bucket, time, to_timestamp(:start_ts)) AS bucket_inner,
            COUNT(*) as count_middle
        FROM passwords
        WHERE
            password = :password
            AND
            to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
        GROUP BY bucket_inner
        ORDER BY bucket_inner
    ) as "raw_timing"
"""

# List of logins by ussages by selected password
logins_of_password_by_usages_list = """
    SELECT
        username,
        COUNT(username) AS count
    FROM passwords
    WHERE
        password = :password
        AND
        to_timestamp(:start_ts) <= time AND time < to_timestamp(:finish_ts)
    GROUP BY username
    ORDER BY count DESC
    LIMIT :limit
"""
