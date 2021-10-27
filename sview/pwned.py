from flask import render_template
from flask import Blueprint, current_app, request, jsonify

pwned = Blueprint("pwned", __name__)


@pwned.route("/index/",methods=["POST","GET"])
def index():
    params = {"server": current_app.config['PWNED_ADDRESS'], "port": current_app.config['PWNED_PORT']}
    return render_template("pwned/pwned.html", conn_params=params)

@pwned.route("/api-info/", methods=["GET"])
def info():
    return render_template("pwned/pwned-api-info.html")
