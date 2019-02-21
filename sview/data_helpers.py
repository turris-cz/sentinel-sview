import json

from .extensions import db
from .extensions import redis


def query_to_json(query, params=None, post_process=None):
    if not params:
        query_params = None
    elif callable(params):
        query_params = params()
    else:
        query_params = params

    result = []

    data = db.session.execute(query, query_params)
    for row in data:
        result.append(dict(row.items()))

    if post_process and callable(post_process):
        # This is experimental feature
        # It would be nice to have better interface
        returned = post_process(result)
        if returned:
            result = returned

    return json.dumps(result)


def get_and_store(key, query, params=None, post_process=None, expire=None):
    json_data = query_to_json(query, params, post_process)
    redis.set(key, json_data, ex=expire)


def get_data(key):
    data = redis.get(key)
    if not data:
        return None
    return json.loads(data.decode("UTF-8"))


def as_map_data(data, key_key, val_key):
    return {i[key_key]: i[val_key] for i in data}
