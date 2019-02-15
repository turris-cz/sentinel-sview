import json

from .extensions import db
from .extensions import redis


def query_to_json(query):
    result = []

    data = db.session.execute(query)
    for row in data:
        result.append(dict(row.items()))

    return json.dumps(result)


def get_and_store(key, query, expire=None):
    json_data = query_to_json(query)
    redis.set(key, json_data, ex=expire)


def get_data(key):
    data = redis.get(key)
    if not data:
        return None
    return json.loads(data.decode("UTF-8"))


def as_map_data(data, key_key, val_key):
    return {i[key_key]: i[val_key] for i in data}
