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
    def __init__(self, job_handler_key):
        job_id = redis.get(job_handler_key)
        self.id = None

        if not job_id:  # It seems that there should be no job under processing.
            self.status = JobStatus.NO_HANDLER
            return

        # The job was recently deployed. We should try to fetch it.
        self.id = job_id.decode("UTF-8")
        job = rq.get_queue().fetch_job(self.id)

        if not job:  # The job already finished or was cleared
            self.status = JobStatus.NO_JOB
            return

        # The job was succesfully fetched. We should inspect it's state.
        self.status = job.get_status()

    def is_alive(self):
        return self.status in [JobStatus.STARTED, JobStatus.QUEUED]

    def is_failed(self):
        return self.status == JobStatus.FAILED


def inspect_jobs(job_prefix):
    queue = rq.get_queue()
    job_handler_keys = redis.keys(f"{job_prefix}*")
    for job_handler_key in job_handler_keys:

        job_id = redis.get(job_handler_key)
        if not job_id:
            continue

        # The job was recently deployed. We should try to fetch it.
        job_id = job_id.decode("UTF-8")
        job_ttl = redis.ttl(job_handler_key)
        job = queue.fetch_job(job_id)

        (_, query_name, period_name) = job_handler_key.decode().split(";")[0:3]
        params = (
            job_handler_key.decode().split(";")[3:] or ""
        )  # Empty string if no params
        if not job:  # The job already finished or was cleared
            yield (
                f"{query_name:>38s} {period_name:<3s} {params} is removed  "
                f"(id={job_id}, handler_ttl={job_ttl})"
            )
            continue

        # The job was succesfully fetched. We should inspect it's state.
        job_status = job.get_status()
        if job.worker_name:  # The job is assigned to a worker
            execution_time = datetime.datetime.utcnow() - job.started_at
            yield (
                f"{query_name:>38s} {period_name:<3s} is {job_status:<8s} "
                f"(id={job_id}, handler_ttl={job_ttl}, worker={job.worker_name}, "
                f"execution_time={execution_time})"
            )

        else:
            yield (
                f"{query_name:>38s} {period_name:<3s} is {job_status:<8s} "
                f"(id={job_id}, handler_ttl={job_ttl})"
            )
