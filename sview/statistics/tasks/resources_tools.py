import json

from ...extensions import redis

from .periods import PERIODS
from .queries import RESOURCE_QUERIES
from .queries import KNOWN_PARAMS
from .tasks import TaskToolbox
from .tasks import REDIS_KEY_SEPARATOR
from .task_helpers import human_readable_bytes

USER_SPECIFIC_RESOURCES = (
    "my_all_incidents_graph",
    "my_top_countries_by_incidents_graph",
    "my_top_traps_by_incidents_graph",
)


class ResourceToolbox(TaskToolbox):
    REDIS_JOB_PREFIX = "sview_job_id_caching"
    REDIS_CACHE_PREFIX = "sview_cached"
    REDIS_REFRESH_TO_PREFIX = "sview_refresh_timeout"
    AVAILABLE_QUERIES = RESOURCE_QUERIES
    AVAILABLE_PERIODS = PERIODS

    @classmethod
    def inspect_cache(cls, clear=False, dry_run=False):
        """View all resource cache keys with cache ttl and size"""
        keys = redis.keys(f"{cls.REDIS_CACHE_PREFIX}*")
        size = 0
        for key in keys:
            data = redis.get(key)
            ttl = redis.ttl(key)
            key = key.decode()
            if data:
                yield f"{'Clearing ' if clear else ''}{key:<55s} ttl={ttl:<6} size={human_readable_bytes(len(data))}"
                if clear and not dry_run:
                    redis.delete(key)
                size += len(data)

        yield ""
        if clear:
            yield "Cleared {} keys, total size: {}".format(
                len(keys), human_readable_bytes(size)
            )
        else:
            yield "Cached resources occupy:  {}".format(human_readable_bytes(size))

    def __init__(self, name, period, params={}):
        self.name = name
        self.query = self.AVAILABLE_QUERIES[name]
        self.data_type = self.query["data_type"]
        self.period = period
        self.params = params

        self.cached_data_key = self.get_cached_data_key()
        super().__init__()

    def get_query(self):
        """Mainly to insert table name"""
        return self.query["query"].format(
            source_table=self.get_source_table(),
        )

    def get_available_data(self):
        precached_result = redis.get(self.cached_data_key)
        if precached_result:
            return json.loads(precached_result.decode("utf-8"))

    def get_cached_data_key(self):
        return (
            self.REDIS_CACHE_PREFIX + REDIS_KEY_SEPARATOR + self.get_redis_key_suffix()
        )
