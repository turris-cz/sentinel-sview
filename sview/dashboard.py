from flask import render_template
from flask import Blueprint

dashboard = Blueprint("dashboard", __name__)


@dashboard.route("/")
def index():
    return render_template("dashboard/home.html")
