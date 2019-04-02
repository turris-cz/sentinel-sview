from flask import Blueprint

from .job_helpers import common_await_view

api = Blueprint("api", __name__)


@api.route("/job/await", methods=["POST"])
def await_job():
    return common_await_view()
