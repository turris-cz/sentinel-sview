from flask import render_template
from flask import Blueprint

from .data_helpers import get_data


passwords = Blueprint("passwords", __name__)


@passwords.route("/")
def index():
    data_keys = [
        "top_passwords_popularity",
        "top_passwords_long",
        "top_usernames_long",
        "top_combinations_long",
    ]

    data = {k: get_data(k) for k in data_keys}

    return render_template("passwords/home.html", **data)
