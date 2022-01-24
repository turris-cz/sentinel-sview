import json

from flask import Blueprint
from flask import request

from pwned_backend import proc_leaked


api = Blueprint("api", __name__)


_HEADERS = {
    'Content-Type': 'application/json; charset=utf-8'
}


@api.route("/pwned/", methods=["POST"])
def pwned_api():
    """Route for selecting passwords from database"""
    if not request.json:
        args = json.loads(request.get_data())
    else:
        args = request.json

    data, code = proc_leaked(**args)
    return data, code, _HEADERS
