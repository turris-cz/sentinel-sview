import base64
import binascii

from flask import render_template
from flask import Blueprint
from flask import request

from .resources import get_resource
from .extensions import influx
from .job_helpers import run_job
from .jobs import password_detail
from .queries import PERIODS


passwords = Blueprint("passwords", __name__)


@passwords.route("/")
def index():
    resource_names = [
        "top_passwords_popularity",
        "top_passwords_long",
        "top_usernames_long",
        "top_combinations_long",
    ]
    params = {"period": request.args.get("period", "1y")}

    resources = {resource_name: get_resource(resource_name, params) for resource_name in resource_names}

    return render_template("passwords/home.html",
                           resource_names=resource_names,
                           periods=PERIODS,
                           active_params=params,
                           resources=resources)


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
