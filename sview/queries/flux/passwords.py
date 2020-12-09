top_passwords = """
    from(bucket: "mybucket")
        |> range(start: -1000h)
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
    from(bucket: "mybucket")
        |> range(start: -1000h)
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
    from(bucket: "mybucket")
        |> range(start: -1000h)
        |> filter(fn: (r) =>r._measurement=="password_count")
        |> sum()
        |> rename(columns: {{"_field": "password", "_value":"count"}})
        |> keep(columns: ["username", "password", "count"])
        |> group()
        |> sort(columns: ["count"], desc: true)
        |> limit(n: {limit})
"""

top_passwords_popularity = """
    top_passwords=from(bucket: "mybucket")
        |> range(start: -1y)
        |> filter(fn: (r)=>r._measurement=="password_count")
        |> group(columns: ["_field"])
        |> sum()
        |> group()
        |> sort(desc:true)
        |> limit(n: {top_n})
        |> tableFind(fn: (key)=>true)
        |> getColumn(column: "_field")

    from(bucket: "mybucket")
        |> range(start: -1y)
        |> filter(fn: (r)=>r._measurement=="password_count" and contains(value: r._field, set:top_passwords))
        |> group()
        |> window(every: 5m)
        |> group(columns: ["_field", "_start"])
        |> sum()
        |> group(columns: ["_start"])
        |> rename(columns: {{"_field": "password", "_value":"count"}})
        |> map(fn:(r) => ({{ r with day: string(v: r._start) }}))
        |> keep(columns: ["day", "count", "password"])
"""
