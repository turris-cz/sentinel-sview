from flask import render_template
from flask import Blueprint

from .data_helpers import get_data
from .job_helpers import run_job, common_await_view
from .jobs import attacker_detail


attackers = Blueprint("attackers", __name__)


@attackers.route("/")
def index():
    data_keys = [
        "map_scores",
        "attackers_trends",
        "top_countries_long",
        "top_ips_long",
    ]

    data = {k: get_data(k) for k in data_keys}

    return render_template("attackers/home.html", **data)


@attackers.route("/details/ip/<string:ip>")
def ip_details(ip):
    data, job_id = run_job("attackers:details:{}".format(ip), attacker_detail, ip=ip)
    if data:
        if not data["found"]:
            return render_template("attackers/not_found.html", ip=ip)

    return render_template("attackers/detail.html", job_id=job_id, ip=ip, data=data)


@attackers.route("/await", methods=["POST"])
def ip_details_wait():
    return common_await_view()
