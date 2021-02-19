from flask import render_template
from flask import Blueprint
from flask import request

from .resources import get_resource
from .queries import PERIODS


dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/")
def index():
    resource_names = [
        "map_scores",
        "attackers",
        "top_countries",
        "top_passwords",
    ]
    params = {"period": request.args.get("period", "1y")}

    resources = {resource_name: get_resource(resource_name, params) for resource_name in resource_names}

    return render_template("dashboard/home.html",
                           resource_names=resource_names,
                           periods=PERIODS,
                           active_params=params,
                           resources=resources)
