from .exceptions import ResourceError
from .extensions import redis
from .jobs import cache_resource
from .periods import PERIODS
from .queries import RESOURCE_QUERIES
from .queries import PRECACHED_RESOURCES
from .resources_tools import ResourceToolbox
from .rlimit import rate_limit_reached
from .tasks import Task

USER_SPECIFIC_RESOURCES = (
    "my_all_incidents_graph",
    "my_top_countries_by_incidents_graph",
    "my_top_traps_by_incidents_graph",
)


class Resource(Task, ResourceToolbox):
    JOB_FUNCTION = cache_resource

    def _queue_job(self, rlimit=False):
        if rlimit and rate_limit_reached():
            raise ResourceError("Too many requests in row")

        return super()._queue_job()

    def suggest_caching(self, rlimit=False, dry_run=False):
        """Enqueue a job when refresh is allowed or check its result when it is
        already enqueued.
        """
        refresh_ttl = redis.ttl(self.refresh_timeout_key)
        is_time_to_refresh = refresh_ttl <= 0  # -1 for no key, -2 for key with no ttl
        cache_ttl = redis.ttl(self.cached_data_key)

        job_state = self.get_job_state()
        if not job_state.is_alive() and (is_time_to_refresh or job_state.is_failed()):
            job_id = None if dry_run else self._queue_job(rlimit=rlimit)
            if dry_run or job_id:
                return (
                    f"Queueing cache {self.name:^38s} {self.period['handle']:>3s} "
                    f"(refresh_ttl={refresh_ttl}, cache_ttl={cache_ttl}, "
                    f"status={job_state.status}) with id={job_id}"
                )
            else:  # Can't acquire job lock. Job may started from another thread or refresh timeouts were not cleared
                job_state = self.get_job_state()
                return (
                    f"Skipping cache {self.name:^38s} {self.period['handle']:>3s} "
                    f"(refresh_ttl={refresh_ttl}, cache_ttl={cache_ttl}, "
                    f"status={job_state.status}, job_id={job_state.id}) (race condition - timeout pending)"
                )

        return (
            f"Skipping cache {self.name:^38s} {self.period['handle']:>3s} "
            f"(refresh_ttl={refresh_ttl}, cache_ttl={cache_ttl}, "
            f"status={job_state.status}, job_id={job_state.id})"
        )


def get_resource(resource_name, params):
    """Return a cached resource or start a job to query & cache it.
    Return either requested resource or None when it is not ready yet.
    Raise an exception in case of invalid resource or invalid parameters.
    """

    if resource_name not in RESOURCE_QUERIES:
        raise ResourceError(f"Unknown resource '{resource_name}'")

    if params["period"] not in PERIODS:
        raise ResourceError("Not a valid period")

    if resource_name in USER_SPECIFIC_RESOURCES and "token" not in params:
        return RESOURCE_QUERIES[resource_name].get("empty_response", [])

    period = PERIODS[params["period"]]
    params = params.copy()
    del params["period"]

    resource = Resource(
        resource_name,
        period,
        params=params,
    )

    resource.suggest_caching(rlimit=True)

    return resource.get_available_data()


def suggest_caching_period(period_name, dry_run=False):
    for resource_name in PRECACHED_RESOURCES:
        resource = Resource(resource_name, PERIODS[period_name])
        yield resource.suggest_caching(dry_run=dry_run)


def suggest_caching(resource_name, period_name, dry_run=False):
    resource = Resource(resource_name, PERIODS[period_name])
    return resource.suggest_caching(dry_run=dry_run)
