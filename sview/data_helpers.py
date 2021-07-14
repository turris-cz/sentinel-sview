import influxdb_client

from .extensions import influx
from .queries import PERIODS
from .queries import RESOURCE_QUERIES


def process_query(resource_name, params):
    query_frame = RESOURCE_QUERIES[resource_name]["query"]
    params.update(RESOURCE_QUERIES[resource_name].get("params", {}))
    params.update({
        "start": PERIODS[params["period"]]["flux_start"],
        "window": PERIODS[params["period"]]["flux_window"],
        "bucket": PERIODS[params["period"]]["bucket"],
    })

    result = []

    full_query = query_frame.format(**params)
    try:
        tables = influx.client.query_api().query(full_query)
    except influxdb_client.rest.ApiException as exc:
        raise Exception(f"Failed to execute query: {full_query}") from exc

    if len(tables) == 0:
        return []
    elif len(tables) > 1:
        raise Exception("Influx returned {} tables (should be 1)".format(len(tables)))
    table = tables[0]

    for flux_record in table.records:
        del flux_record.values["result"]  # Can't be filtered using flux query
        del flux_record.values["table"]  # Can't be filtered using flux query
        result.append(flux_record.values)

    post_process = RESOURCE_QUERIES[resource_name].get("post_process")
    if post_process and callable(post_process):
        # This is experimental feature
        # It would be nice to have better interface
        returned = post_process(result)
        if returned:
            result = returned

    return result
