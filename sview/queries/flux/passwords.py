top_passwords = """
    from(bucket: "sentinel-base")
        |> range(start: {start})
        |> filter(fn: (r) =>r._measurement=="password_count")
        |> group(columns:["_field"])
        |> sum()
        |> rename(columns: {{"_field": "password", "_value":"count"}})
        |> keep(columns: ["password", "count"])
        |> group()
        |> sort(columns: ["count"], desc: true)
        |> limit(n: {limit})
"""

top_usernames = """
    from(bucket: "sentinel-base")
        |> range(start: {start})
        |> filter(fn: (r) =>r._measurement=="password_count")
        |> group(columns:["username"])
        |> sum()
        |> rename(columns: {{"_value": "count"}})
        |> keep(columns: ["username", "count"])
        |> group()
        |> sort(columns: ["count"], desc: true)
        |> limit(n: {limit})
"""

top_combinations = """
    from(bucket: "sentinel-base")
        |> range(start: {start})
        |> filter(fn: (r) =>r._measurement=="password_count")
        |> sum()
        |> rename(columns: {{"_field": "password", "_value":"count"}})
        |> keep(columns: ["username", "password", "count"])
        |> group()
        |> sort(columns: ["count"], desc: true)
        |> limit(n: {limit})
"""

top_passwords_popularity = """
    top_passwords=from(bucket: "sentinel-base")
        |> range(start: {start})
        |> filter(fn: (r)=>r._measurement=="password_count")
        |> group(columns: ["_field"])
        |> sum()
        |> group()
        |> sort(desc:true)
        |> limit(n: {top_n})
        |> findColumn(fn: (key)=>true, column: "_field")

    from(bucket: "sentinel-base")
        |> range(start: {start})
        |> filter(fn: (r)=>r._measurement=="password_count" and contains(value: r._field, set:top_passwords))
        |> group()
        |> window(every: {window})
        |> group(columns: ["_field", "_start"])
        |> sum()
        |> group(columns: ["_start"])
        |> rename(columns: {{"_field": "password", "_value":"count"}})
        |> map(fn:(r) => ({{ r with day: string(v: r._start) }}))
        |> keep(columns: ["day", "count", "password"])
"""

password_activity_graph = """
    from(bucket: "sentinel-base")
        |> range(start: -1y)
        |> filter(fn: (r) =>r._measurement=="password_count" and r._field=="{password}")
        |> group()
        |> window(every: 1w)
        |> sum()
        |> rename(columns: {{"_value":"count"}})
        |> map(fn:(r) => ({{ r with day: string(v: r._start) }}))
        |> keep(columns: ["day", "count"])
        |> group()
"""
logins_of_password = """
    from(bucket: "sentinel-base")
        |> range(start: -1y)
        |> filter(fn: (r) =>r._measurement=="password_count" and r._field=="{password}")
        |> group(columns: ["username"])
        |> sum()
        |> group()
        |> sort(desc: true)
        |> limit(n: 20)
        |> rename(columns: {{"_value":"count"}})
        |> keep(columns: ["username", "count"])
"""
