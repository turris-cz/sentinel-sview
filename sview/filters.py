import os

from flask import current_app


def autoversion_filter(filename):
    if not current_app.debug:
        return filename

    fullpath = os.path.join(current_app.root_path, filename[1:])
    try:
        timestamp = str(int(os.path.getmtime(fullpath)))
    except OSError:
        return filename

    return "{}?={}".format(filename, timestamp)


def register_filters(app):
    app.jinja_env.filters["autoversion"] = autoversion_filter
