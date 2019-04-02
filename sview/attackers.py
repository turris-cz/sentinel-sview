import datetime

from flask import render_template
from flask import Blueprint

from .data_helpers import get_data
from .job_helpers import run_job
from .jobs import attacker_detail, day_detail


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


_DATE_FORMAT = "%Y-%m-%d"


def _parse_day(day):
    try:
        dt = datetime.datetime.strptime(day, _DATE_FORMAT)
    except ValueError:
        return None

    return dt


def _next_day_str(day):
    dt = _parse_day(day)
    next_day = dt + datetime.timedelta(days=1)

    return next_day.strftime(_DATE_FORMAT)


def _previous_day_str(day):
    dt = _parse_day(day)
    prev_day = dt - datetime.timedelta(days=1)

    return prev_day.strftime(_DATE_FORMAT)


@attackers.route("/details/day/")
@attackers.route("/details/day/<string:day>")
def day_details(day=None):
    if not day or not _parse_day(day):
        return "Day must be specified. Do not edit links manually.", 400

    data, job_id = run_job("attackers:day_details:{}".format(day), day_detail, day=day)
    if data:
        if not data["found"]:
            return render_template("attackers/not_found.html", day=day)

    next_day = _next_day_str(day)
    prev_day = _previous_day_str(day)

    run_job("attackers:day_details:{}".format(next_day), day_detail, _count=False, day=next_day)
    run_job("attackers:day_details:{}".format(prev_day), day_detail, _count=False, day=prev_day)

    return render_template("attackers/day.html",
                           job_id=job_id,
                           day=day,
                           data=data,
                           next_day=next_day,
                           previous_day=prev_day
                           )
