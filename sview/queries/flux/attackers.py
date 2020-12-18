attacker_ips = """
    from(bucket: "sentinel-base")
        |> range(start: -1y)
        |> filter(fn: (r) =>r._measurement=="attacker_count")
        |> group(columns:["_field"])
        |> sum()
        |> rename(columns: {{"_field":"ip", "_value":"count"}})
        |> keep(columns: ["ip", "count"])
        |> group()
        |> sort(columns: ["count"], desc: true)
        |> limit(n: {limit})
"""

attackers_by_day = """
    from(bucket: "sentinel-base")
        |> range(start: -1y)
        |> filter(fn: (r) =>r._measurement=="attacker_count")
        |> group()
        |> window(every: 1w)
        |> unique(column: "_field")
        |> sum()
        |> rename(columns: {{"_value":"count"}})
        |> map(fn:(r) => ({{ r with day: string(v: r._start) }}))
        |> keep(columns: ["day", "count"])
        |> group()
"""

attackers_activity_graph = """
    from(bucket: "sentinel-base")
        |> range(start: -1y)
        |> filter(fn: (r) =>r._measurement=="attacker_count" and r._field=="{ip}")
        |> group()
        |> window(every: 1w)
        |> sum()
        |> rename(columns: {{"_value":"count"}})
        |> map(fn:(r) => ({{ r with day: string(v: r._start) }}))
        |> keep(columns: ["day", "count"])
        |> group()
"""
