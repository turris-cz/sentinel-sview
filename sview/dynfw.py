from flask import render_template
from flask import Blueprint, current_app

dynfw = Blueprint("dynfw", __name__)


@dynfw.route("/dynfw/")
def index():
    data = {
        "server": current_app.config["DYNFW_SOCKET_ADDR"],
        "port": current_app.config["DYNFW_SOCKET_PORT"],
    }
    return render_template("dynfw/dynfw.html", dynfwhost=data)
