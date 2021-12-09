import base64
import binascii
import re

from flask import jsonify
from flask import render_template
from flask import Blueprint
from flask import redirect
from flask import request
from flask import session
from flask import url_for
from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumb

from .exceptions import ResourceError
from .resources import get_resource
from .periods import PERIODS, DEFAULT_PERIOD
from .queries import KNOWN_PARAMS
from .view_helpers import get_tokens_hash
from .view_helpers import endpoint_arguments_constructor

statistics = Blueprint("statistics", __name__)
default_breadcrumb_root(statistics, ".")

DEVICE_TOKEN_CHARS = "^[a-z0-9]*$"
DEVICE_TOKEN_LENGTH = 64


@statistics.route("/")
@register_breadcrumb(
    statistics,
    ".",
    "Overview",
    endpoint_arguments_constructor=endpoint_arguments_constructor,
)
def dashboard():
    page_title = "Overview"
    resource_names = [
        "all_countries_by_incidents_list",
        "all_attackers_graph",
        "all_incidents_graph",
        "top_countries_by_incidents_list",
        "top_passwords_by_usages_list",
    ]
    period = request.args.get("period")
    if period not in PERIODS:
        return redirect(url_for(request.endpoint, period=DEFAULT_PERIOD))

    params = {"period": period}

    resources = {
        resource_name: get_resource(resource_name, params)
        for resource_name in resource_names
    }

    return render_template(
        "statistics/dashboard.html",
        resource_names=resource_names,
        periods=PERIODS,
        active_params=params,
        resources=resources,
        page_title=page_title,
    )


@statistics.route("/attackers/")
@register_breadcrumb(
    statistics,
    ".attacker",
    "Attackers",
    endpoint_arguments_constructor=endpoint_arguments_constructor,
)
def attackers():
    page_title = "Attackers"
    resource_names = [
        "all_countries_by_attackers_list",
        "all_attackers_graph",
        "top_countries_by_attackers_graph",
        "top_countries_by_attackers_list_long",
        "top_attackers_by_incidents_list_long",
    ]
    period = request.args.get("period")
    if period not in PERIODS:
        return redirect(url_for(request.endpoint, period=DEFAULT_PERIOD))

    params = {"period": period}

    resources = {
        resource_name: get_resource(resource_name, params)
        for resource_name in resource_names
    }

    return render_template(
        "statistics/attackers.html",
        resource_names=resource_names,
        periods=PERIODS,
        active_params=params,
        resources=resources,
        page_title=page_title,
    )


@statistics.route("/attackers/details/ip/<string:ip>")
@register_breadcrumb(
    statistics,
    ".attacker.ip",
    "Attacker Details",
    endpoint_arguments_constructor=endpoint_arguments_constructor,
)
def attacker_details(ip):
    page_title = "Attacker Details"
    resource_names = [
        "selected_attacker_incidents_graph",
    ]
    period = request.args.get("period")
    if period not in PERIODS:
        return redirect(url_for(request.endpoint, ip=ip, period=DEFAULT_PERIOD))

    params = {
        "period": period,
        "ip": ip,
    }

    resources = {
        resource_name: get_resource(resource_name, params)
        for resource_name in resource_names
    }

    return render_template(
        "statistics/attacker_details.html",
        resource_names=resource_names,
        periods=PERIODS,
        active_params=params,
        resources=resources,
        page_title=page_title,
    )


@statistics.route("/passwords/")
@register_breadcrumb(
    statistics,
    ".passwords",
    "Passwords",
    endpoint_arguments_constructor=endpoint_arguments_constructor,
)
def passwords():
    page_title = "Passwords"
    resource_names = [
        "top_passwords_by_usages_graph",
        "top_passwords_by_usages_list_long",
        "top_usernames_by_usages_list_long",
        "top_combinations_by_usages_list_long",
    ]
    period = request.args.get("period")
    if period not in PERIODS:
        return redirect(url_for(request.endpoint, period=DEFAULT_PERIOD))

    params = {"period": period}

    resources = {
        resource_name: get_resource(resource_name, params)
        for resource_name in resource_names
    }

    return render_template(
        "statistics/passwords.html",
        resource_names=resource_names,
        periods=PERIODS,
        active_params=params,
        resources=resources,
        page_title=page_title,
    )


def _decode_password(encoded_password):
    try:
        return str(base64.b64decode(encoded_password), "UTF-8")
    except (binascii.Error, UnicodeDecodeError):
        return None


@statistics.route("/passwords/details/<string:encoded_password>")
@register_breadcrumb(
    statistics,
    ".passwords.details",
    "Password Details",
    endpoint_arguments_constructor=endpoint_arguments_constructor,
)
def password_details(encoded_password):
    page_title = "Password Details"
    password = _decode_password(encoded_password)
    if not password:
        return "Unable to decode password", 400

    resource_names = [
        "logins_of_password_by_usages_list",
        "selected_password_by_usages_graph",
    ]
    period = request.args.get("period")
    if period not in PERIODS:
        return redirect(
            url_for(
                request.endpoint,
                encoded_password=encoded_password,
                period=DEFAULT_PERIOD,
            )
        )

    params = {
        "period": period,
        "password": password,
    }

    resources = {
        resource_name: get_resource(resource_name, params)
        for resource_name in resource_names
    }

    return render_template(
        "statistics/password_details.html",
        resource_names=resource_names,
        periods=PERIODS,
        active_params=params,
        resources=resources,
        page_title=page_title,
    )


@statistics.route("/incidents/")
@register_breadcrumb(
    statistics,
    ".incidents",
    "Incidents",
    endpoint_arguments_constructor=endpoint_arguments_constructor,
)
def incidents():
    page_title = "Incidents"
    resource_names = [
        "all_countries_by_incidents_list",
        "all_incidents_graph",
        "top_countries_by_incidents_list",
        "top_incident_types_by_incidents_list",
        "top_countries_by_incidents_graph",
        "top_traps_by_incidents_graph",
        "top_actions_by_incidents_graph",
    ]
    period = request.args.get("period")
    if period not in PERIODS:
        return redirect(url_for(request.endpoint, period=DEFAULT_PERIOD))

    params = {"period": period}

    resources = {
        resource_name: get_resource(resource_name, params)
        for resource_name in resource_names
    }

    return render_template(
        "statistics/incidents.html",
        resource_names=resource_names,
        periods=PERIODS,
        active_params=params,
        resources=resources,
        page_title=page_title,
    )


@statistics.route("/ports/")
@register_breadcrumb(
    statistics,
    ".ports",
    "Ports",
    endpoint_arguments_constructor=endpoint_arguments_constructor,
)
def ports():
    page_title = "Ports"
    resource_names = [
        "all_ports_by_scans_graph",
        "top_ports_by_scans_list_long",
        "top_ports_by_scans_graph",
    ]
    period = request.args.get("period")
    if period not in PERIODS:
        return redirect(url_for(request.endpoint, period=DEFAULT_PERIOD))

    params = {"period": period}

    resources = {
        resource_name: get_resource(resource_name, params)
        for resource_name in resource_names
    }

    return render_template(
        "statistics/ports.html",
        resource_names=resource_names,
        periods=PERIODS,
        active_params=params,
        resources=resources,
        page_title=page_title,
    )


@statistics.route("/devices/")
@register_breadcrumb(
    statistics,
    ".devices",
    "My Devices",
    endpoint_arguments_constructor=endpoint_arguments_constructor,
)
def devices():
    page_title = "My Devices"
    resource_names = [
        "my_all_incidents_graph",
        "my_top_traps_by_incidents_graph",
        "my_top_countries_by_incidents_graph",
    ]
    tokens_hash = get_tokens_hash(session.get("devices"))

    period = request.args.get("period")
    if period not in PERIODS:
        return redirect(
            url_for(request.endpoint, period=DEFAULT_PERIOD, token=tokens_hash)
        )

    if tokens_hash != request.args.get("token"):
        return redirect(url_for(request.endpoint, period=period, token=tokens_hash))

    params = (
        {"period": period, "token": tokens_hash} if tokens_hash else {"period": period}
    )

    tokens = tuple(session.get("devices", []))

    resources = {
        resource_name: get_resource(
            resource_name, {**params, "my_device_tokens": tokens}
        )
        for resource_name in resource_names
    }

    return render_template(
        "statistics/devices.html",
        resource_names=resource_names,
        periods=PERIODS,
        active_params=params,
        resources=resources,
        page_title=page_title,
    )


@statistics.route("/api/resource")
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
        response.cache_control.max_age = PERIODS[params["period"]]["user_cache_ttl"]

    return response


@statistics.route("/api/device/<action>", methods=["POST"])
def device_view(action):
    if action not in ("add", "delete"):
        return "Unknown operation", 500

    if "device_token" not in request.form:
        return "Device token not provided", 400

    period = request.form.get("period", DEFAULT_PERIOD)
    if period not in PERIODS:
        period = DEFAULT_PERIOD

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
        return redirect(url_for("statistics.devices", period=period, token=token))

    else:
        return redirect(url_for("statistics.devices", period=period))
