from flask import render_template
from flask import Blueprint

from .data_helpers import get_data, as_map_data


dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/")
def index():
    data_keys = [
        "top_passwords",
        "top_usernames",
        "top_countries",
        "top_combinations",
        "map_scores",
        "attackers",
    ]

    data = {k: get_data(k) for k in data_keys}

    if data["map_scores"]:
        data["map_scores"] = as_map_data(data["map_scores"], "country", "count")

    return render_template("dashboard/home.html", **data)
