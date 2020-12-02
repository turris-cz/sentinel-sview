attacker_ips = """
    from(bucket: "mybucket")
        |> range(start: -1000h)
        |> filter(fn: (r) =>r._measurement=="attacker_count")
        |> group(columns:["_field"])
        |> sum()
        |> rename(columns: {{"_field":"ip", "_value":"count"}})
        |> keep(columns: ["ip", "count"])
        |> group()
        |> sort(columns: ["count"], desc: true)
        |> limit(n: {limit})
"""
