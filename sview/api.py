from flask import Blueprint
from flask import jsonify
from flask import request

from .exceptions import ResourceError
from .resources import get_resource
from .job_helpers import common_await_view

api = Blueprint("api", __name__)


@api.route("/job/await", methods=["POST"])
def await_job():
    return common_await_view()


@api.route("/resource")
def get_resource_view():
    resource_name = request.args.get("name")
    if resource_name is None:
        return jsonify({"error": "No resource name privided."})

    period = request.args.get("period", "1y")

    try:
        return jsonify({
            "resource_name": resource_name,
            "data": get_resource(resource_name, period)
        })
    except ResourceError as exc:
        return jsonify({"error": str(exc)})
