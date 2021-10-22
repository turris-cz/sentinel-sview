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
        now() - INTERVAL :interval < time AND time < now()
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
        now() - INTERVAL :interval < time AND time < now()
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
        now() - INTERVAL :interval < time AND time < now()
    GROUP BY username, password
    ORDER BY count DESC
    LIMIT :limit
"""

# Graph of top passwords by ussages
top_passwords_by_usages_graph = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS day,
        password,
        COUNT(*) as count
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
                    now() - INTERVAL :interval < time AND time < now()
                GROUP BY password
                ORDER BY count_inner DESC
                LIMIT :limit
            ) AS foo
        )
        AND
        now() - INTERVAL :interval < time AND time < now()
    GROUP BY day, password
    ORDER BY day
"""

# Graph of selected passwords's ussages
selected_password_by_usages_graph = """
    SELECT
        to_char(time_bucket(:bucket, time), 'YYYY-MM-DD HH24:MI') AS day,
        COUNT(*) as count
    FROM passwords
    WHERE
        password = :password
        AND
        now() - INTERVAL :interval < time AND time < now()
    GROUP BY day
    ORDER BY day
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
        now() - INTERVAL :interval < time AND time < now()
    GROUP BY username
    ORDER BY count DESC
"""
