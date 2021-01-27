from flask import render_template
from flask import Blueprint

from .resources import get_resource


dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/")
def index():
    resource_names = [
        "map_scores",
        "attackers",
        "top_countries",
        "top_passwords",
    ]

    resources = {resource_name: get_resource(resource_name) for resource_name in resource_names}

    return render_template("dashboard/home.html", **resources)
