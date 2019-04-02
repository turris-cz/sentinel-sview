import base64
import binascii

from flask import render_template
from flask import Blueprint

from .data_helpers import get_data
from .job_helpers import run_job
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


def _decode_password(encoded_password):
    try:
        return str(base64.b64decode(encoded_password), "UTF-8")
    except (binascii.Error, UnicodeDecodeError):
        return None


@passwords.route("/details/<string:encoded_password>")
def password_details(encoded_password):
    password = _decode_password(encoded_password)
    if not password:
        return "Unable to decode password", 400

    data, job_id = run_job("passwords:details:{}".format(encoded_password),
                           password_detail,
                           password=password)
    if data:
        if not data["found"]:
            return render_template("passwords/not_found.html", password=password)

    return render_template("passwords/detail.html", job_id=job_id, password=password, data=data)
