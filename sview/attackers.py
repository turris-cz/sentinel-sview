from flask import request, render_template, jsonify
from flask import Blueprint

from .extensions import rq

from .jobs import run_job, attacker_detail
from .data_helpers import get_data


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
    data, await_job = run_job("attackers:details:{}".format(ip), attacker_detail, ip=ip)

    return render_template("attackers/detail.html", await_job=await_job, ip=ip, data=data)


@attackers.route("/await", methods=["POST"])
def ip_details_wait():
    job_id = request.form.get("job_id")
    job = rq.get_queue().fetch_job(job_id)

    if not job:
        return jsonify({"error": "Waiting for nonexistent job"}), 404

    if job.is_failed:
        return jsonify({"error": "Server error during request processing"}), 500

    if job.is_finished:
        return jsonify({"job_done": True})
    else:
        return jsonify({"job_done": False})
