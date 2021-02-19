import datetime

from flask import jsonify, request

from .extensions import redis, rq
from .rlimit import rlimit


def run_job(handler, job_function,  **kwargs):
    """Enqueue a job or check its result when it is already enqueued.
    Return either (job.result, None) when the job already finished or
    (None, job.id) when it is still pending.
    """
    @rlimit
    def _queue_job(job_function, **kw):
        job = job_function.queue(**kw)
        redis.set(_job_handler_key(handler), job.id, ex=job.result_ttl)
        return job.id

    job_id = redis.get(_job_handler_key(handler))
    if job_id:
        job_id = job_id.decode("UTF-8")
    else:
        return None, _queue_job(job_function, **kwargs)

    job = rq.get_queue().fetch_job(job_id)
    if not job:
        return None, _queue_job(job_function, **kwargs)

    # Data are returned only in case that job finished.  Other cases will
    # generate the AJAX call to determine what happened.
    #
    # I can't decide if this is hack or nice solution. It solves all the
    # problems and reuses a bunch of code. The straightforward approach needs
    # more variables or more checks in the view function. So, for now, I vote
    # for this one
    if job.is_finished:
        return job.result, None

    return None, job.id


def _job_waits_too_long(started):
    now = datetime.datetime.utcnow()
    if now - started > datetime.timedelta(seconds=10):
        return True

    return False


def _job_handler_key(handler):
    return "job_id:{}".format(handler)
def mark_data_with_found(d):
    found = True
    for v in d.values():
        if v:
            break
    else:
        found = False

    d["found"] = found
