import base64
import binascii

from flask import render_template
from flask import Blueprint
from flask import request

from .resources import get_resource
from .queries import PERIODS


statistics = Blueprint("statistics", __name__)


@statistics.route("/")
def dashboard():
    resource_names = [
        "incidents_map",
        "attackers",
        "all_incidents_graph",
        "top_countries_by_incidents_table",
        "top_passwords",
    ]
    params = {"period": request.args.get("period", "1y")}

    resources = {resource_name: get_resource(resource_name, params) for resource_name in resource_names}

    return render_template("statistics/dashboard.html",
                           resource_names=resource_names,
                           periods=PERIODS,
                           active_params=params,
                           resources=resources)


@statistics.route("/attackers/")
def attackers():
    resource_names = [
        "attackers_map",
        "attackers",
        "attackers_trends",
        "top_countries_by_attackers_table_long",
        "top_ips_long",
    ]
    params = {"period": request.args.get("period", "1y")}

    resources = {resource_name: get_resource(resource_name, params) for resource_name in resource_names}

    return render_template("statistics/attackers.html",
                           resource_names=resource_names,
                           periods=PERIODS,
                           active_params=params,
                           resources=resources)


@statistics.route("/attackers/details/ip/<string:ip>")
def attacker_details(ip):
    resource_names = [
        "attacker_activity",
    ]
    params = {
        "period": request.args.get("period", "1y"),
        "ip": ip
    }

    resources = {resource_name: get_resource(resource_name, params) for resource_name in resource_names}

    return render_template("statistics/attacker_details.html",
                           resource_names=resource_names,
                           periods=PERIODS,
                           active_params=params,
                           resources=resources)


@statistics.route("/passwords/")
def passwords():
    resource_names = [
        "top_passwords_popularity",
        "top_passwords_long",
        "top_usernames_long",
        "top_combinations_long",
    ]
    params = {"period": request.args.get("period", "1y")}

    resources = {resource_name: get_resource(resource_name, params) for resource_name in resource_names}

    return render_template("statistics/passwords.html",
                           resource_names=resource_names,
                           periods=PERIODS,
                           active_params=params,
                           resources=resources)


def _decode_password(encoded_password):
    try:
        return str(base64.b64decode(encoded_password), "UTF-8")
    except (binascii.Error, UnicodeDecodeError):
        return None


@statistics.route("/passwords/details/<string:encoded_password>")
def password_details(encoded_password):
    password = _decode_password(encoded_password)
    if not password:
        return "Unable to decode password", 400

    resource_names = [
        "password_logins",
        "password_in_time",
    ]
    params = {
        "period": request.args.get("period", "1y"),
        "password": password,
    }

    resources = {resource_name: get_resource(resource_name, params) for resource_name in resource_names}

    return render_template("statistics/password_details.html",
                           resource_names=resource_names,
                           periods=PERIODS,
                           active_params=params,
                           resources=resources)


@statistics.route("/incidents/")
def incidents():
    resource_names = [
        "incidents_map",
        "all_incidents_graph",
        "top_countries_by_incidents_table",
        "top_incident_types",
        "incidents_by_country_trends",
        "incidents_by_source_trends",
        "incidents_by_action_trends",
    ]
    params = {"period": request.args.get("period", "1y")}

    resources = {resource_name: get_resource(resource_name, params) for resource_name in resource_names}

    return render_template("statistics/incidents.html",
                           resource_names=resource_names,
                           periods=PERIODS,
                           active_params=params,
                           resources=resources)


@statistics.route("/ports/")
def ports():
    resource_names = [
        "all_scans_graph",
        "top_ports_long",
        "port_trends",
    ]
    params = {"period": request.args.get("period", "1y")}

    resources = {resource_name: get_resource(resource_name, params) for resource_name in resource_names}

    return render_template("statistics/ports.html",
                           resource_names=resource_names,
                           periods=PERIODS,
                           active_params=params,
                           resources=resources)


@statistics.route("/devices/")
def devices():
    resource_names = [
        "my_incidents_graph",
    ]
    params = {"period": request.args.get("period", "1y")}

    if "devices" in session:
        params["my_device_tokens"] = str(session["devices"]).replace("'", '"')
    else:
        params["my_device_tokens"] = "[]"

    resources = {resource_name: get_resource(resource_name, params) for resource_name in resource_names}

    return render_template("statistics/devices.html",
                           resource_names=resource_names,
                           periods=PERIODS,
                           active_params=params,
                           resources=resources)
