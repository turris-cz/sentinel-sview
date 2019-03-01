from flask import jsonify, request

from .extensions import redis, rq


def run_job(handler, job_function,  **kwargs):
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
