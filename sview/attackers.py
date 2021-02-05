from flask import render_template
from flask import Blueprint
from flask import request

from .resources import get_resource
from .queries import PERIODS


attackers = Blueprint("attackers", __name__)


@attackers.route("/")
def index():
    resource_names = [
        "map_scores",
        "attackers_trends",
        "top_countries_long",
        "top_ips_long",
    ]
    params = {"period": request.args.get("period", "1y")}

    resources = {resource_name: get_resource(resource_name, params) for resource_name in resource_names}

    return render_template("attackers/home.html",
                           resource_names=resource_names,
                           periods=PERIODS,
                           active_params=params,
                           resources=resources)


@attackers.route("/details/ip/<string:ip>")
def ip_details(ip):
    resource_names = [
        "attacker_activity",
    ]
    params = {
        "period": request.args.get("period", "1y"),
        "ip": ip
    }

    resources = {resource_name: get_resource(resource_name, params) for resource_name in resource_names}

    return render_template("attackers/detail.html",
                           resource_names=resource_names,
                           periods=PERIODS,
                           active_params=params,
                           resources=resources)
