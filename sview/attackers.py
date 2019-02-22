from flask import render_template
from flask import Blueprint

from .data_helpers import get_data


attackers = Blueprint("attackers", __name__)


@attackers.route("/")
def index():
    data_keys = [
        "map_scores",
        "attackers_trends",
        "top_countries_long",
    ]

    data = {k: get_data(k) for k in data_keys}

    return render_template("attackers/home.html", **data)
