import json

from flask import render_template, Blueprint, request, jsonify

from password_checker import process_request

pass_check = Blueprint("pcheck", __name__)
apiv1 = Blueprint("apiv1", __name__)


@pass_check.route("/", methods=["POST", "GET"])
def index_pwned():
    page_title = "Sentinel Password Checker"
    return render_template(
        "password_checker/password_check.html", page_title=page_title
    )


@apiv1.route("/", methods=["POST", "GET"])
def endpoint():
    """Route for accessing database"""
    if request.is_json:
        data, code = process_request(**request.json)
        return jsonify(data), code
    else:
        return (
            jsonify(
                {"API error": "Invalid HTTP method for URL Please use the POST method."}
            ),
            400,
        )


@apiv1.route("/doc", methods=["GET"])
def info():
    """Route providing"""
    page_title = "Sentinel Password Checker API"
    return render_template("password_checker/api-info.html", page_title=page_title)


pass_check.register_blueprint(apiv1, url_prefix="/apiv1")
