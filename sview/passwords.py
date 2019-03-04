import base64

from flask import render_template
from flask import Blueprint

from .data_helpers import get_data
from .job_helpers import run_job, common_await_view
from .jobs import password_detail


passwords = Blueprint("passwords", __name__)


@passwords.route("/")
def index():
    data_keys = [
        "top_passwords_popularity",
        "top_passwords_long",
        "top_usernames_long",
        "top_combinations_long",
    ]

    data = {k: get_data(k) for k in data_keys}

    return render_template("passwords/home.html", **data)


@passwords.route("/details/<string:encoded_password>")
def password_details(encoded_password):
    password = str(base64.b64decode(encoded_password), "UTF-8")

    data, job_id = run_job("passwords:details:{}".format(encoded_password),
                           password_detail,
                           password=password)
    if data:
        if not data["found"]:
            return render_template("passwords/not_found.html", password=password)

    return render_template("passwords/detail.html", job_id=job_id, password=password, data=data)


@passwords.route("/await", methods=["POST"])
def password_details_wait():
    return common_await_view()
