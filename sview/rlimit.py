from flask import current_app, request, abort

from functools import wraps

from .extensions import redis


# OK, This is very poor class but I don't want to duplicate some pieces of code
class RLimit():
    def __init__(self):
        self.ban_time = current_app.config["RLIMIT_BAN_TIME"]
        self.max_hits = current_app.config["RLIMIT_MAX_HITS"]
        self.key = "rate-limit:{}:{}".format(request.endpoint, request.remote_addr)

    def count(self):
        pipe = redis.pipeline(transaction=True)
        pipe.set(self.key, 0, ex=self.ban_time, nx=True)
        pipe.incr(self.key)
        pipe.expire(self.key, self.ban_time)
        pipe_result = pipe.execute()

        hits = (pipe_result[1])
        if hits > self.max_hits:
            self._ban()

    def is_enabled(self):
        hits_redis = redis.get(self.key)
        hits = 0 if not hits_redis else int(hits_redis)
        if hits and hits > self.max_hits:
            return False
        return True

    def _ban(self):
        redis.expire(self.key, self.ban_time)


def rlimit(f):
    @wraps(f)
    def _rlimit(*args, **kwargs):
        rl = RLimit()
        if rl.is_enabled():
            rl.count()
            return f(*args, **kwargs)

        return abort(400, "You hit the rate limit")

    return _rlimit
