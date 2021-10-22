import base64
import binascii

from flask import render_template
from flask import Blueprint
from flask import redirect
from flask import request
from flask import session
from flask import url_for

from .resources import get_resource
from .queries import PERIODS, DEFAULT_PERIOD
from .view_helpers import get_tokens_hash
from flask_breadcrumbs import default_breadcrumb_root, register_breadcrumb


statistics = Blueprint("statistics", __name__)
default_breadcrumb_root(statistics, ".")


@statistics.route("/")
@register_breadcrumb(statistics, ".", "Overview")
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
@register_breadcrumb(statistics, ".attacker", "Attackers")
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
@register_breadcrumb(statistics, ".attacker.ip", "Attacker Details")
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
@register_breadcrumb(statistics, ".passwords", "Passwords")
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
@register_breadcrumb(statistics, ".passwords.details", "Password Details")
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
@register_breadcrumb(statistics, ".incidents", "Incidents")
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
@register_breadcrumb(statistics, ".ports", "Ports")
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
@register_breadcrumb(statistics, ".devices", "My Devices")
def devices():
    page_title = "My Devices"
    resource_names = [
        "my_all_incidents_graph",
        "my_top_traps_by_incidents_graph",
        "my_top_countries_by_incidents_graph",
    ]
    tokens_hash = get_tokens_hash(session.get("devices"))

    period = request.args.get("period")
    if period not in PERIODS or tokens_hash != request.args.get("token"):
        return redirect(
            url_for(request.endpoint, period=DEFAULT_PERIOD, token=tokens_hash)
        )

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
