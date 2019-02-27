from .extensions import redis, rq

from .queries import QUERIES


@rq.job(result_ttl=10)
def load_data_from_template(resource_name):
    from .data_helpers import get_and_store
    get_and_store(resource_name,
                  QUERIES[resource_name]["query"],
                  params=QUERIES[resource_name].get("params"),
                  post_process=QUERIES[resource_name].get("post_process"))


@rq.job(result_ttl=300)
def attacker_detail(**kwargs):
    from .data_helpers import process_query
    from .queries import _attacker_activity_during_time, _attacker_passwords

    return {
        "attacker_activity": process_query(_attacker_activity_during_time, params=kwargs),
        "attacker_passwords": process_query(_attacker_passwords, params=kwargs),
    }


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
