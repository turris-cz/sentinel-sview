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
