from flask import Blueprint
from flask import jsonify
from flask import request

from .exceptions import ResourceError
from .resources import get_resource
from .resources import KNOWN_PARAMS

api = Blueprint("api", __name__)


@api.route("/resource")
def get_resource_view():
    resource_name = request.args.get("name")
    if resource_name is None:
        return jsonify({"error": "No resource name provided."})

    params = {}
    for param_name, default_value in KNOWN_PARAMS.items():
        param = request.args.get(param_name, default_value)
        if param is not None:
            params[param_name] = param

    try:
        return jsonify({
            "resource_name": resource_name,
            "data": get_resource(resource_name, params)
        })
    except ResourceError as exc:
        return jsonify({"error": str(exc)})
