all_incidents_graph = """
    from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r) =>r._measurement=="incident_count")
        |> group()
        |> window(every: {window})
        |> sum()
        |> rename(columns: {{"_value":"count"}})
        |> map(fn:(r) => ({{ r with day: string(v: r._start) }}))
        |> keep(columns: ["day", "count"])
"""

top_incident_types = """
    from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r) =>r._measurement=="incident_count")
        |> group(columns:["_field", "action"])
        |> sum()
        |> group()
        |> sort(columns: ["_value"], desc: true)
        |> rename(columns: {{"_field": "source", "_value": "count"}})
        |> keep(columns: ["source", "action", "count"])
        |> limit(n: {limit})
"""

incidents_by_source_trends = """
    top_sources=from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r)=>r._measurement=="incident_count")
        |> group(columns: ["_field"])
        |> sum()
        |> group()
        |> sort(desc:true)
        |> limit(n: {top_n})
        |> findColumn(fn: (key)=>true, column: "_field")

    from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r)=>r._measurement=="incident_count"
            and contains(value: r._field, set:top_sources)
            )
        |> group()
        |> window(every: {window})
        |> group(columns: ["_field", "_start"])
        |> sum()
        |> group(columns: ["_start"])
        |> rename(columns: {{"_value":"count", "_field": "source"}})
        |> map(fn:(r) => ({{ r with day: string(v: r._start) }}))
        |> keep(columns: ["day", "count", "source"])
"""


incidents_by_action_trends = """
    top_actions=from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r)=>r._measurement=="incident_count" and exists r.action)
        |> group(columns: ["action"])
        |> sum()
        |> group()
        |> sort(desc:true)
        |> limit(n: {top_n})
        |> findColumn(fn: (key)=>true, column: "action")

    from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r)=>r._measurement=="incident_count"
            and exists r.action
            and contains(value: r.action, set:top_actions)
            )
        |> group()
        |> window(every: {window})
        |> group(columns: ["action", "_start"])
        |> sum()
        |> group(columns: ["_start"])
        |> rename(columns: {{"_value":"count"}})
        |> map(fn:(r) => ({{ r with day: string(v: r._start) }}))
        |> keep(columns: ["day", "count", "action"])
"""
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
my_incidents_by_country_trends = """
    top_countries=from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r)=>r._measurement=="user_incident_count"
            and exists r.country
            and contains(value: r._field, set: {my_device_tokens})
            )
        |> group(columns: ["country"])
        |> sum()
        |> group()
        |> sort(desc:true)
        |> limit(n: {top_n})
        |> findColumn(fn: (key)=>true, column: "country")

    from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r)=>r._measurement=="user_incident_count"
            and exists r.country
            and contains(value: r.country, set:top_countries)
            and contains(value: r._field, set: {my_device_tokens})
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

my_incidents_by_source_trends = """
    top_sources=from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r)=>r._measurement=="user_incident_count"
            and contains(value: r._field, set: {my_device_tokens})
            and exists r.source
            )
        |> group(columns: ["source"])
        |> sum()
        |> group()
        |> sort(desc:true)
        |> limit(n: {top_n})
        |> findColumn(fn: (key)=>true, column: "source")

    from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r)=>r._measurement=="user_incident_count"
            and contains(value: r.source, set:top_sources)
            and contains(value: r._field, set: {my_device_tokens})
            )
        |> group()
        |> window(every: {window})
        |> group(columns: ["source", "_start"])
        |> sum()
        |> group(columns: ["_start"])
        |> rename(columns: {{"_value":"count"}})
        |> map(fn:(r) => ({{ r with day: string(v: r._start) }}))
        |> keep(columns: ["day", "count", "source"])
"""

my_incidents_graph = """
    from(bucket: "{bucket}")
        |> range(start: {start})
        |> filter(fn: (r) =>r._measurement=="user_incident_count"
            and contains(value: r._field, set: {my_device_tokens})
            )
        |> group()
        |> window(every: {window})
        |> sum()
        |> rename(columns: {{"_value":"count"}})
        |> map(fn:(r) => ({{ r with day: string(v: r._start) }}))
        |> keep(columns: ["day", "count"])
"""
