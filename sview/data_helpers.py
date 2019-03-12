import json

from .extensions import db, redis


def process_query(query, params=None, post_process=None):
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

    return result


def query_to_json(query, params=None, post_process=None):
    result = process_query(query, params, post_process)
    return json.dumps(result)


def get_and_store(key, query, params=None, post_process=None, expire=None):
    json_data = query_to_json(query, params, post_process)
    redis.set(key, json_data, ex=expire)


def get_data(key):
    data = redis.get(key)
    if not data:
        return None
    return json.loads(data.decode("UTF-8"))


class TaskError(Exception):
    pass


class TaskResult:
    def __init__(self, data):
        self._data = data

    def serialize(self):
        return json.dumps(self._data).encode()

    @classmethod
    def deserialize(cls, raw_data):
        data = json.loads(raw_data.decode("UTF-8"))
        return cls(data)

    @property
    def data(self):
        return self._data

    @property
    def json(self):
        return json.dumps(self._data)

    def __getattr__(self, item):
        if item == "data":
            return self._data
        else:
            return self._data[item]


class DBMultiTask:
    def __init__(self, name, expire=None, params=None):
        self._name = name
        self._expire = expire
        self._params = params
        self._data = None
        self._definitions = {}

    def from_dict(self, name, task_definition):
        if "query" not in task_definition:
            raise TaskError("Missing mandatory item 'query'")
        self._definitions[name] = DBTask(name,
                                         task_definition["query"],
                                         expire=task_definition.get("expire"),
                                         params=task_definition.get("params"),
                                         post_process=task_definition.get("post_process"))

    def store(self):
        redis.set(self._name, TaskResult(self._data).serialize(), ex=self._expire)

    @staticmethod
    def load(name):
        serialized = redis.get(name)
        if not serialized:
            return None
        return TaskResult.deserialize(serialized)

    @classmethod
    def fetch(cls, name):
        result = cls.load(name)
        if not result:
            return None
        return result.data

    @property
    def data(self):
        return TaskResult(self._data)

    def process(self, *args, **kwargs):
        data = self._process(*args, **kwargs)
        returned = self._post_process(data)
        if returned:
            self._data = returned
        else:
            self._data = data

    def _process(self, *args, **kwargs):
        params = {}
        if self._params:
            if callable(self._params):
                params.update(self._params())
            else:
                params.update(self._params)
        params.update(kwargs)

        result = []

        data = db.session.execute(self._query, params)
        for row in data:
            result.append(dict(row.items()))

        return result

    def _post_process(self, data):
        if self._post_process_callback:
            return self._post_process_callback(data)

        return None


class DBTask:
    def __init__(self, name, query, expire=None, params=None, post_process=None):
        self._name = name
        self._query = query
        self._expire = expire
        self._params = params
        self._data = None
        if post_process and not callable(post_process):
            raise TaskError("post_process is not callable")
        self._post_process_callback = post_process

    @classmethod
    def from_dict(cls, name, task_definition):
        if "query" not in task_definition:
            raise TaskError("Missing mandatory item 'query'")
        return cls(name,
                   task_definition["query"],
                   expire=task_definition.get("expire"),
                   params=task_definition.get("params"),
                   post_process=task_definition.get("post_process"))

    def store(self):
        redis.set(self._name, TaskResult(self._data).serialize(), ex=self._expire)

    @staticmethod
    def load(name):
        serialized = redis.get(name)
        if not serialized:
            return None
        return TaskResult.deserialize(serialized)

    @classmethod
    def fetch(cls, name):
        result = cls.load(name)
        if not result:
            return None
        return result.data

    @property
    def data(self):
        return TaskResult(self._data)

    def process(self, *args, **kwargs):
        data = self._process(*args, **kwargs)
        returned = self._post_process(data)
        if returned:
            self._data = returned
        else:
            self._data = data

    def _process(self, *args, **kwargs):
        params = {}
        if self._params:
            if callable(self._params):
                params.update(self._params())
            else:
                params.update(self._params)
        params.update(kwargs)

        result = []

        data = db.session.execute(self._query, params)
        for row in data:
            result.append(dict(row.items()))

        return result

    def _post_process(self, data):
        if self._post_process_callback:
            return self._post_process_callback(data)

        return None
