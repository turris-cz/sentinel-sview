import json

from flask import render_template
from flask import Blueprint

from flask import request
from password_checker import proc_leaked

pass_check = Blueprint("pcheck", __name__)
apiv1 = Blueprint("apiv1", __name__)

_HEADERS = {"Content-Type": "application/json; charset=utf-8"}


@pass_check.route("/", methods=["POST", "GET"])
def index_pwned():
    page_title = "Sentinel Password Checker"
    return render_template(
        "password_checker/password_check.html", page_title=page_title
    )


@apiv1.route("/", methods=["POST"])
def endpoint():
    """Route for accessing database"""
    if not request.json:
        args = json.loads(request.get_data())
    else:
        args = request.json

    data, code = proc_leaked(**args)
    return data, code, _HEADERS


@apiv1.route("/doc", methods=["GET"])
def info():
    """Route providing"""
    page_title = "Sentinel Password Checker API"
    return render_template("password_checker/api-info.html", page_title=page_title)


pass_check.register_blueprint(apiv1, url_prefix="/apiv1")
