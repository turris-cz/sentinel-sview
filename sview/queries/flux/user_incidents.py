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

