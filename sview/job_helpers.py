from flask import jsonify, request

from .extensions import redis, rq
from .rlimit import rlimit


def run_job(handler, job_function,  **kwargs):
    @rlimit
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

    # This if solves a weird behavior of page reloads. If job fails, it is
    # reported trough AJAX and the error message is shown. But, if user reloads
    # page there are only empty data. This if reports failed job in the same
    # manner as started job.  After this, macro runs the AJAX request and this
    # request is able to dig out the fact that job's been failed.
    #
    # I can't decide if this is hack or nice solution. It solves problem and
    # reuse a bunch of code. The straightforward approach needs more variables
    # or more checks in the view function. So, for now, I vote for this one
    if job.is_failed:
        return None, job.id

    return job.result, None


def common_await_view(post_name="job_id"):
    job_id = request.form.get(post_name)
    job = rq.get_queue().fetch_job(job_id)

    if not job:
        return jsonify({"error": "Waiting for nonexistent job"}), 404

    if job.is_failed:
        return jsonify({"error": "Server error during request processing"}), 500

    if job.is_finished:
        return jsonify({"job_done": True})
    else:
        return jsonify({"job_done": False})


def check_and_mark_data_with_found(d):
    found = True
    for v in d.values():
        if v:
            break
    else:
        found = False

    d["found"] = found
