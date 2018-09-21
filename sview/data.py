from flask import render_template
from flask import Blueprint


databp = Blueprint("data", __name__)


@databp.route("/")
def index():
    return render_template("index.html")
