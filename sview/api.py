import re

from flask import Blueprint
from flask import jsonify
from flask import redirect
from flask import request
from flask import url_for
from flask import session

from .exceptions import ResourceError
from .resources import get_resource
from .queries import KNOWN_PARAMS
from .queries import PERIODS, DEFAULT_PERIOD
from .view_helpers import get_tokens_hash

api = Blueprint("api", __name__)

DEVICE_TOKEN_CHARS = "^[a-z0-9]*$"
DEVICE_TOKEN_LENGTH = 64


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

    if "devices" in session:
        params["my_device_tokens"] = tuple(session["devices"])

    try:
        data = get_resource(resource_name, params)
    except ResourceError as exc:
        return jsonify({"error": str(exc)})

    response = jsonify(
        {
            "resource_name": resource_name,
            "data": data,
        }
    )

    if data is not None:
        response.cache_control.max_age = PERIODS[params["period"]]["cache_ttl"]

    return response


@api.route("/device/<action>", methods=["POST"])
def device_view(action):
    if action not in ("add", "delete"):
        return "Unknown operation", 500

    if "device_token" not in request.form:
        return "Device token not provided", 400

    if (
        not re.match(DEVICE_TOKEN_CHARS, request.form["device_token"])
        or len(request.form["device_token"]) != DEVICE_TOKEN_LENGTH
    ):
        return "Bad format of device token", 400

    if "devices" not in session:
        session["devices"] = []

    if action == "add":
        if request.form["device_token"] not in session["devices"]:
            session["devices"].append(request.form["device_token"])
            session.modified = True

    elif action == "delete":
        if request.form["device_token"] in session["devices"]:
            session["devices"].remove(request.form["device_token"])
            session.modified = True

    token = get_tokens_hash(session.get("devices"))
    if token:
        return redirect(
            url_for("statistics.devices", period=DEFAULT_PERIOD, token=token)
        )

    else:
        return redirect(url_for("statistics.devices", period=DEFAULT_PERIOD))
