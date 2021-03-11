import json

from .extensions import redis, influx
from .queries import PERIODS


def process_query(query, period, params=None, post_process=None):
    if not params:
        query_params = {}
    elif callable(params):
        query_params = params()
    else:
        query_params = params

    query_params.update({
        "start": PERIODS[period]["flux_start"],
        "window": PERIODS[period]["flux_window"],
        "bucket": PERIODS[period]["bucket"],
    })

    result = []

    tables = influx.client.query_api().query(query.format(**query_params))

    if len(tables) == 0:
        return []
    elif len(tables) > 1:
        raise Exception("Influx returned {} tables (should be 1)".format(len(tables)))
    table = tables[0]

    for flux_record in table.records:
        del flux_record.values["result"]  # Can't be filtered using flux query
        del flux_record.values["table"]  # Can't be filtered using flux query
        result.append(flux_record.values)

    if post_process and callable(post_process):
        # This is experimental feature
        # It would be nice to have better interface
        returned = post_process(result)
        if returned:
            result = returned

    return result

def precached_data_key(resource_name, period):
    return "precached:{}:{}".format(resource_name, period)
