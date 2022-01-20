from flask import render_template
from flask import Blueprint, current_app, request, jsonify, url_for
from sview.api import pwned_api as _pwnd

pwned = Blueprint("pwned", __name__)


@pwned.route("/index/",methods=["POST","GET"])
def index():
    params = {"path": request.host + "/api/pwned/"}
    return render_template("pwned/pwned.html", conn_params=params)


@pwned.route("/api-info/", methods=["GET"])
def info():
    return render_template("pwned/pwned-api-info.html")

