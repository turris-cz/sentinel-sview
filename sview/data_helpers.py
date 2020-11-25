import json

from .extensions import db, redis, influx
from .queries import DEFAULT_BACKEND


def process_query(query, params=None, post_process=None, backend=DEFAULT_BACKEND):
    if not params:
        query_params = None
    elif callable(params):
        query_params = params()
    else:
        query_params = params

    result = []

    if backend == "sqalchemy":
        data = db.session.execute(query, query_params)
        for row in data:
            result.append(dict(row.items()))

    elif backend == "influx":
        table = influx.client.query_api().query(query.format(**query_params))[0]

        for flux_record in table.records:
            del flux_record.values["result"]  # Can't be filtered using flux query
            del flux_record.values["table"]  # Can't be filtered using flux query
            result.append(flux_record.values)

    else:
        raise Exception("Unsupported backend: {}".format(backend))

    if post_process and callable(post_process):
        # This is experimental feature
        # It would be nice to have better interface
        returned = post_process(result)
        if returned:
            result = returned

    return result


def query_to_json(query, backend, params=None, post_process=None):
    result = process_query(query, params, post_process, backend)
    return json.dumps(result)


def get_and_store(key, query, params=None, post_process=None, expire=None,
                  backend=DEFAULT_BACKEND):
    json_data = query_to_json(query, backend, params, post_process)
    redis.set(key, json_data, ex=expire)


def get_data(key):
    data = redis.get(key)
    if not data:
        return None
    return json.loads(data.decode("UTF-8"))
