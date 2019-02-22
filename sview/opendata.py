from flask import render_template
from flask import Blueprint


opendata = Blueprint("opendata", __name__)


@opendata.route("/")
def index():
    return render_template("opendata/home.html")
