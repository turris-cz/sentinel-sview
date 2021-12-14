from ...extensions import redis

from .queries import KNOWN_PARAMS
from .periods.time import utc_now_ts
from .periods.time import LAST_TS_BEFORE_FUNCTIONS
from .job_helpers import JobState
from .task_helpers import is_ip, is_token_hash

REDIS_PLACEHOLDER = "1"  # Shall only return logical true
JOB_TIMEOUT = 60 * 60  # Seconds


def guess_params_from_redis_handler(job_handler):
    """All the redis handlers have the same format prefix;query_name;period;params"""
    handler_parts = job_handler.split(";")

    query_name = handler_parts[1]
    period_name = handler_parts[2]
    params_list = handler_parts[3:]  # optional - like ip, password or device token hash
    params = {}
    for param in params_list:
        if is_ip(param):
            params["ip"] = param
        elif is_token_hash(param):
            params["token"] = param
        else:
            params["password"] = param

    return query_name, period_name, params


class TaskToolbox:
    @classmethod
    def from_job_handler(cls, job_handler):
        query_name, period_name, params = guess_params_from_redis_handler(job_handler)
        if query_name in cls.AVAILABLE_QUERIES and period_name in cls.AVAILABLE_PERIODS:
            return cls(query_name, cls.AVAILABLE_PERIODS[period_name], params)

    @classmethod
    def inspect_jobs(cls):
        job_handler_keys = redis.keys(f"{cls.REDIS_JOB_PREFIX}*")
        info_logs = []
        for job_handler_key in job_handler_keys:
            job_handler = job_handler_key.decode()
            task = cls.from_job_handler(job_handler)
            info_logs.append(task.get_job_info())

        for log in sorted(info_logs, key=lambda item: item.get("index")):
            yield (
                f"{log['name']:<38s} {log['period']:<9s} "
                f"{log['params'] or ''} {log['info']}"
            )

    @classmethod
    def inspect_timeouts(cls, period_name=None, clear=False, dry_run=False):
        """Inspect refresh timeouts assigned to all tasks. Timeouts could be also
        cleared or restricted to selected period. If dry run is enabled, nothing
        is cleared."""
        if period_name is None:
            period_name = "*"
        keys = redis.keys(f"{cls.REDIS_REFRESH_TO_PREFIX};*;{period_name}")
        timeout_logs = []
        for key in keys:
            ttl = redis.ttl(key)
            query_name, period_name, params = guess_params_from_redis_handler(
                key.decode()
            )
            timeout_log = {
                "key": key,
                "ttl": ttl,
                "name": query_name,
                "period": period_name,
                "params": params,
                "index": cls.AVAILABLE_PERIODS[period_name]["index"],  # for sorting
            }
            timeout_logs.append(timeout_log)

        for log in sorted(timeout_logs, key=lambda item: item.get("index")):
            yield (
                f"{'Clearing ' if clear else ''}{log['name']:<38s} "
                f"{log['period']:<9s} ttl={log['ttl']:<6} params={log['params']}"
            )
            if clear and not dry_run:
                redis.delete(log["key"])

        if clear:
            yield ""
            yield f"Cleared {len(timeout_logs)} refresh timeouts"

    def __init__(self):
        self.job_handler_key = self.get_job_handler_key()
        self.refresh_timeout_key = self.get_refresh_timeout_key()
        if (
            "last_ts_before_function" in self.period
        ):  # it's absent in native period which is not aggregated
            self.get_last_ts_before = LAST_TS_BEFORE_FUNCTIONS[
                self.period.get("last_ts_before_function")
            ]

    def get_job_info(self):
        job_state = self.get_job_state()
        info = {
            "name": self.name,
            "period": self.period["handle"],
            "params": self.params,
            "index": self.period["index"],  # for sorting
            "info": job_state.get_info(),
        }
        return info

    def get_start_delay(self):
        period = self.period
        start_delay = 0
        while period["source_period"] is not None:
            start_delay += period["start_delay_bonus"]
            period = period["source_period"]

        return start_delay

    def get_refresh_timeout(self):
        return (
            self.get_last_ts_before(-self.period["refresh_interval"])
            - utc_now_ts()
            + self.get_start_delay()
        )

    def get_start_ts(self):
        return self.get_last_ts_before(self.period["display_interval"])

    def get_finish_ts(self):
        return self.get_last_ts_before()

    def get_source_table(self):
        return f"{self.data_type}_{self.period['source_period']['handle']}".strip("_")

    def get_query_params(self):
        query_params = self.params.copy()
        query_params.update(self.query.get("params", {}))
        query_params.update(
            {
                "bucket": self.period["bucket"],
                "finish_ts": self.get_finish_ts(),
                "start_ts": self.get_start_ts(),
            }
        )
        return query_params

    def get_job_state(self):
        return JobState(self.job_handler_key, self.period["queue"])

    def get_job_handler_key(self):
        return "{};{}".format(
            self.REDIS_JOB_PREFIX,
            ";".join(
                [self.name, self.period["handle"]]
                + [
                    v
                    for k, v in self.params.items()
                    if k in KNOWN_PARAMS and v is not None
                ]
            ),
        )

    def get_refresh_timeout_key(self):
        return "{};{}".format(
            self.REDIS_REFRESH_TO_PREFIX,
            ";".join(
                [self.name, self.period["handle"]]
                + [
                    v
                    for k, v in self.params.items()
                    if k in KNOWN_PARAMS and v is not None
                ]
            ),
        )


class Task(TaskToolbox):
    def _queue_job(self):
        refresh_timeout = self.get_refresh_timeout()
        # refresh timeout not set because it already exists
        race_condition = not redis.set(
            self.refresh_timeout_key, REDIS_PLACEHOLDER, nx=True, ex=refresh_timeout
        )
        if race_condition:
            return
        job = self.JOB_FUNCTION.queue(
            self.name, self.period, self.params, queue=self.period["queue"]
        )
        redis.set(self.job_handler_key, job.id, ex=JOB_TIMEOUT)
        return job.id
