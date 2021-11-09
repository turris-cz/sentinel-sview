import sqlalchemy
import re

from flask import current_app

from .extensions import db
from .queries import PERIODS
from .queries import RESOURCE_QUERIES


class QueryFiller:
    def __init__(self, query_frame, params):
        self.query_frame = query_frame
        self.params = params

    def __str__(self):
        return _fill_query(self.query_frame, self.params)


def _fill_query(query, params):
    """Fill params into sql query. Omly for debug purposes."""

    def replace(match):
        param_name = match.group(0)[1:]
        if param_name == "MI":
            return ":MI"

        try:
            param = params[param_name]
        except KeyError:
            raise Exception(f"Unknown param '{param_name}' requested in query: {query}")

        if type(param) is str:
            return f"'{param}'"
        elif type(param) is int or type(param) is tuple:
            return str(param)
        else:
            raise Exception(
                f"""Unsupported param type of '{param_name}' requested
                    in query: {query}\n. The available params are: {params}"""
            )

    return re.sub(r":[\w_]+", replace, query)


def process_query(resource_name, params):
    query = RESOURCE_QUERIES[resource_name]["query"]
    params.update(RESOURCE_QUERIES[resource_name].get("params", {}))
    params["bucket"] = PERIODS[params["period"]]["bucket"]
    params["finish_ts"] = PERIODS[params["period"]]["get_finish"]()
    params["start_ts"] = PERIODS[params["period"]]["get_start"]()

    result = []

    try:
        current_app.logger.debug(
            "Fetching resource '%s' with query: %s",
            resource_name,
            QueryFiller(query, params),
        )
        data = db.session.execute(query, params)
    except sqlalchemy.exc.SQLAlchemyError as exc:
        full_query = _fill_query(query, params)
        raise Exception(f"Failed to execute query: {full_query}") from exc

    for row in data:
        result.append(dict(row))

    post_process = RESOURCE_QUERIES[resource_name].get("post_process")
    if post_process and callable(post_process):
        # This is experimental feature
        # It would be nice to have better interface
        returned = post_process(result)
        if returned:
            result = returned

    return result
