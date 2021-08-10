attacker_ips = """
    from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r) =>r._measurement=="attacker_incident_count")
        |> group(columns:["_field"])
        |> sum()
        |> rename(columns: {{"_field":"ip", "_value":"count"}})
        |> keep(columns: ["ip", "count"])
        |> group()
        |> sort(columns: ["count"], desc: true)
        |> limit(n: {limit})
"""

attackers_by_day = """
    from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r) =>r._measurement=="attacker_incident_count")
        |> group()
        |> window(every: {window})
        |> unique(column: "_field")
        |> sum()
        |> rename(columns: {{"_value":"count"}})
        |> map(fn:(r) => ({{ r with day: string(v: r._start) }}))
        |> keep(columns: ["day", "count"])
        |> group()
"""

attackers_activity_graph = """
    from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r) =>r._measurement=="attacker_incident_count" and r._field=="{ip}")
        |> group()
        |> window(every: {window})
        |> sum()
        |> rename(columns: {{"_value":"count"}})
        |> map(fn:(r) => ({{ r with day: string(v: r._start) }}))
        |> keep(columns: ["day", "count"])
        |> group()
"""

top_countries_by_incidents_table = """
    from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r) =>r._measurement=="attacker_incident_count" and exists r.country)
        |> group(columns:["country"])
        |> sum()
        |> rename(columns: {{"_value":"count"}})
        |> keep(columns: ["country", "count"])
        |> group()
        |> sort(columns: ["count"], desc: true)
        |> limit(n: {limit})
"""

top_countries_by_attackers_table = """
    from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r) =>r._measurement=="attacker_incident_count" and exists r.country)
        |> group(columns:["country"])
        |> unique(column: "_field")
        |> sum()
        |> rename(columns: {{"_value":"count"}})
        |> keep(columns: ["country", "count"])
        |> group()
        |> sort(columns: ["count"], desc: true)
        |> limit(n: {limit})
"""

incidents_map = """
    from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r) =>r._measurement=="attacker_incident_count" and exists r.country)
        |> group(columns:["country"])
        |> sum()
        |> rename(columns: {{"_value":"count"}})
        |> keep(columns: ["country", "count"])
        |> group()
"""

attackers_map = """
    from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r) =>r._measurement=="attacker_incident_count" and exists r.country)
        |> group(columns:["country"])
        |> unique(column: "_field")
        |> sum()
        |> rename(columns: {{"_value":"count"}})
        |> keep(columns: ["country", "count"])
        |> group()
"""

top_countries_trends = """
    top_countries=from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r)=>r._measurement=="attacker_incident_count" and exists r.country)
        |> group(columns: ["country"])
        |> unique(column: "_field")
        |> sum()
        |> group()
        |> sort(desc:true)
        |> limit(n: {top_n})
        |> findColumn(fn: (key)=>true, column: "country")

    from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r)=>r._measurement=="attacker_incident_count"
            and exists r.country
            and contains(value: r.country, set:top_countries)
            )
        |> group()
        |> window(every: {window})
        |> unique(column: "_field")
        |> group(columns: ["country", "_start"])
        |> sum()
        |> group(columns: ["_start"])
        |> rename(columns: {{"_value":"count"}})
        |> map(fn:(r) => ({{ r with day: string(v: r._start) }}))
        |> keep(columns: ["day", "count", "country"])
"""

incidents_by_country_trends = """
    top_countries=from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r)=>r._measurement=="attacker_incident_count" and exists r.country)
        |> group(columns: ["country"])
        |> sum()
        |> group()
        |> sort(desc:true)
        |> limit(n: {top_n})
        |> findColumn(fn: (key)=>true, column: "country")

    from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r)=>r._measurement=="attacker_incident_count"
            and exists r.country
            and contains(value: r.country, set:top_countries)
            )
        |> group()
        |> window(every: {window})
        |> group(columns: ["country", "_start"])
        |> sum()
        |> group(columns: ["_start"])
        |> rename(columns: {{"_value":"count"}})
        |> map(fn:(r) => ({{ r with day: string(v: r._start) }}))
        |> keep(columns: ["day", "count", "country"])
"""
