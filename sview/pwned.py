from flask import render_template
from flask import Blueprint, current_app, request, jsonify

pwned = Blueprint("pwned", __name__)


@pwned.route("/api/",methods=["POST","GET"])
def index():
    data = {"server": current_app.config['PWNED_ADDRESS'], "port": current_app.config['PWNED_PORT']}
    return render_template("pwned/pwned.html", pwned_connection=data)
