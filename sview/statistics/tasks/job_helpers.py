import datetime

from ...extensions import redis
from ...extensions import rq


class JobStatus:
    """All possible states of sview jobs. A combination of redis queue job
    states (listed at https://python-rq.org/docs/jobs/) and two sview special
    states: NO_HANDLER and NO_JOB
    """

    NO_HANDLER = "no handler"
    NO_JOB = "no job"
    STARTED = "started"
    QUEUED = "queued"
    FAILED = "failed"
    FINISHED = "finished"
    UNDEFINED = "undefined"


class JobState:
    def __init__(self, job_handler_key, queue):
        self.handler = job_handler_key
        job_id = redis.get(job_handler_key)
        self.queue = queue
        self.id = None

        if not job_id:  # It seems that there should be no job under processing.
            self.status = JobStatus.NO_HANDLER
            return

        # The job was recently deployed. We should try to fetch it.
        self.id = job_id.decode("UTF-8")
        job = rq.get_queue(self.queue).fetch_job(self.id)

        if not job:  # The job already finished or was cleared
            self.status = JobStatus.NO_JOB
            return

        # The job was succesfully fetched. We should inspect it's state.
        self.job = job
        self.status = self.job.get_status()

    def is_alive(self):
        return self.status in [JobStatus.STARTED, JobStatus.QUEUED]

    def is_failed(self):
        return self.status == JobStatus.FAILED

    def get_info(self):
        if self.status == JobStatus.NO_HANDLER:
            return "handler key just expired"

        handler_ttl = redis.ttl(self.handler)
        if self.status == JobStatus.NO_JOB:
            return f"is removed  (id={self.id}, handler_ttl={handler_ttl})"

        # The job was succesfully fetched. We should inspect it's state.
        if self.job.worker_name:  # The job is assigned to a worker
            execution_time = datetime.datetime.utcnow() - self.job.started_at
            return (
                f"is {self.status:<8s} (id={self.id}, handler_ttl={handler_ttl}, "
                f"worker={self.job.worker_name}, execution_time={execution_time})"
            )

        else:
            return f"is {self.status:<8s} (id={self.id}, handler_ttl={handler_ttl})"
