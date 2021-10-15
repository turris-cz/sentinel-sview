from flask import Flask, request
from .database import load_dev

from .backend import proc_leaked, proc_leaked_advanced

app = Flask(__name__)
# temporary
load_dev()


@app.route("/api/leaked/", methods=["POST"])
def leaked():
    """Route to select from database without hashed"""
    return proc_leaked(**request.json)


@app.route("/api/leaked_advanced/", methods=["POST"])
def leaked_advanced():
    """Route for selecting passwords from advanced database"""
    return proc_leaked_advanced(**request.json)
