from flask import render_template
from flask import Blueprint

from .data_helpers import get_data


dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/")
def index():
    data_keys = [
        "top_passwords",
        "top_usernames",
        "top_countries",
        "top_combinations",
    ]

    data = {k: get_data(k) for k in data_keys}

    return render_template("dashboard/home.html", **data)
