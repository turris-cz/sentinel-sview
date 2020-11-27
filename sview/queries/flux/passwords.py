top_passwords = """
    from(bucket: "bucket2")
        |> range(start: -1000h)
        |> filter(fn: (r) =>r._measurement=="logins")
        |> group(columns:["password"])
        |> sum()
        |> duplicate(column: "_value", as: "count")
        |> keep(columns: ["password", "count"])
        |> group()
        |> sort(columns: ["count"], desc: true)
        |> limit(n: {limit})
"""
