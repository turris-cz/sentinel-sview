from flask import render_template
from flask import Blueprint

web = Blueprint("web", __name__)


@web.route("/greylist-data/")
def greylist():
    return render_template("greylist-data/index.html")
