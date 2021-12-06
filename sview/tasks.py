from .extensions import redis

from .queries import KNOWN_PARAMS
from .queries.time import utc_now_ts
from .queries.time import LAST_TS_BEFORE_FUNCTIONS
from .job_helpers import JobState

REDIS_PLACEHOLDER = "1"  # Shall only return logical true
JOB_TIMEOUT = 600  # Seconds


class TaskToolbox:
    def __init__(self):
        self.job_handler_key = self.get_job_handler_key()
        self.refresh_timeout_key = self.get_refresh_timeout_key()
        if (
            "last_ts_before_function" in self.period
        ):  # it's absent in native period which is not aggregated
            self.get_last_ts_before = LAST_TS_BEFORE_FUNCTIONS[
                self.period.get("last_ts_before_function")
            ]

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
        return JobState(self.job_handler_key)

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
        job = self.JOB_FUNCTION.queue(self.name, self.period, self.params)
        redis.set(self.job_handler_key, job.id, ex=JOB_TIMEOUT)
        return job.id
