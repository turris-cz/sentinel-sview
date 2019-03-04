import os
import base64

import pycountry

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


def country_code_to_name(cc):
    c = pycountry.countries.get(alpha_2=cc)
    return c.common_name if hasattr(c, "common_name") else c.name


def base64_encode(s):
    return base64.b64encode(bytes(s, "UTF-8"))


def register_filters(app):
    app.jinja_env.filters["autoversion"] = autoversion_filter
    app.jinja_env.filters["uncc"] = country_code_to_name
    app.jinja_env.filters["b64"] = base64_encode
