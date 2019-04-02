import datetime

from flask import jsonify, request

from .extensions import redis, rq
from .rlimit import rlimit


def run_job(handler, job_function, _count=True, **kwargs):
    @rlimit(_count)
    def _queue_job(job_function, **kw):
        job = job_function.queue(**kw)
        redis.set(handler, job.id, ex=job.result_ttl)
        return job.id

    job_id = redis.get(handler)
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


def common_await_view(post_name="job_id"):
    job_id = request.form.get(post_name)
    job = rq.get_queue().fetch_job(job_id)

    if not job:
        return jsonify({"error": "Waiting for nonexistent job"}), 404

    if job.is_failed:
        return jsonify({"error": "Server error during request processing"}), 500

    if job.is_started:
        response = {
            "job_done": False,
            "job_started": True,
            "status": "Processing of your request has been started...",
        }
        return jsonify(response)

    if job.is_finished:
        return jsonify({"job_done": True})

    if _job_waits_too_long(job.enqueued_at):
        response = {
            "job_done": False,
            "job_started": False,
            "warning": "Your request is waiting too long for processing. There may be a problem with server.",
        }
        return jsonify(response)

    # This may be a dead branch of code, but it's a bullet-proof solution.
    return jsonify({"job_done": False, "job_started": False})


def mark_data_with_found(d):
    found = True
    for v in d.values():
        if v:
            break
    else:
        found = False

    d["found"] = found
