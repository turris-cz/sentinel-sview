from flask import render_template
from flask import Blueprint
from flask import request

from .resources import get_resource
from .job_helpers import run_job
from .jobs import attacker_detail
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
    period = request.args.get("period", "1y")

    resources = {resource_name: get_resource(resource_name, period) for resource_name in resource_names}

    return render_template("attackers/home.html",
                           periods=PERIODS,
                           active_period=period,
                           **resources)


@attackers.route("/details/ip/<string:ip>")
def ip_details(ip):
    data, job_id = run_job("attackers:details:{}".format(ip), attacker_detail, ip=ip)
    if data:
        if not data["found"]:
            return render_template("attackers/not_found.html", ip=ip)

    return render_template("attackers/detail.html", job_id=job_id, ip=ip, data=data)


