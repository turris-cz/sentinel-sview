from .extensions import db
from .queries import PERIODS
from .queries import RESOURCE_QUERIES


def process_query(resource_name, params):
    query_frame = RESOURCE_QUERIES[resource_name]["query"]
    params.update(RESOURCE_QUERIES[resource_name].get("params", {}))
    params["interval"] = PERIODS[params["period"]]["interval"]
    params["bucket"] = PERIODS[params["period"]]["bucket"]

    result = []

    full_query = query_frame.format(**params)
    try:
        data = db.session.execute(full_query)
    except Exception as exc:
        raise Exception(f"Failed to execute query: {full_query}") from exc
    for row in data:
        result.append(dict(row.items()))

    post_process = RESOURCE_QUERIES[resource_name].get("post_process")
    if post_process and callable(post_process):
        # This is experimental feature
        # It would be nice to have better interface
        returned = post_process(result)
        if returned:
            result = returned

    return result
