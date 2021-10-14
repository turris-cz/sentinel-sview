import re
from flask import Flask, request
from base import load_dev

from base.models import Password

app = Flask(__name__)
load_dev()


@app.route("/api/register/", methods=['POST'])
def index():
    

    pass


@app.route("/api/leaked/", methods=["POST"])
def leaked():
    pwd = request.json["password"]
    q = Password.select().where(Password.password == pwd)
    if q.count() < 1:
        return {"status": "SAFE"}, 200
    else:
        res = q.get().count
        return {"status": "USED", "count": res}, 200
    return 500
