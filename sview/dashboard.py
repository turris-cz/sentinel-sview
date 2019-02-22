from flask import render_template
from flask import Blueprint

from .data_helpers import get_data


dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/")
def index():
    data_keys = [
        "map_scores",
        "attackers",
        "top_countries",
        "top_passwords",
    ]

    data = {k: get_data(k) for k in data_keys}

    return render_template("dashboard/home.html", **data)
