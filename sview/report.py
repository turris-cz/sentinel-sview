from flask import render_template, Blueprint

report = Blueprint("report", __name__)


@report.route("/report")
def info():
    return render_template("report/report.html")
