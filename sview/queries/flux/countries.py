top_countries = """
    from(bucket: "mybucket")
        |> range(start: -1000h)
        |> filter(fn: (r) =>r._measurement=="minipot_count")
        |> group(columns:["country"])
        |> sum()
        |> rename(columns: {{"_value":"count"}})
        |> keep(columns: ["country", "count"])
        |> group()
        |> sort(columns: ["count"], desc: true)
        |> limit(n: {limit})
"""

map_overview = """
    from(bucket: "mybucket")
        |> range(start: -1000h)
        |> filter(fn: (r) =>r._measurement=="minipot_count")
        |> group(columns:["country"])
        |> sum()
        |> rename(columns: {{"_value":"count"}})
        |> keep(columns: ["country", "count"])
        |> group()
"""

top_countries_trends = """
    top_countries=from(bucket: "mybucket")
        |> range(start: -1y)
        |> filter(fn: (r)=>r._measurement=="attacker_count")
        |> group(columns: ["country"])
        |> unique(column: "_field")
        |> sum()
        |> group()
        |> sort(desc:true)
        |> limit(n: {top_n})
        |> findColumn(fn: (key)=>true, column: "country")

    from(bucket: "mybucket")
        |> range(start: -1y)
        |> filter(fn: (r)=>r._measurement=="attacker_count" and contains(value: r.country, set:top_countries))
        |> group()
        |> window(every: 5m)
        |> unique(column: "_field")
        |> group(columns: ["country", "_start"])
        |> sum()
        |> group(columns: ["_start"])
        |> rename(columns: {{"_value":"count"}})
        |> map(fn:(r) => ({{ r with day: string(v: r._start) }}))
        |> keep(columns: ["day", "count", "country"])
"""
