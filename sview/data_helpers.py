import sqlalchemy
import re

from flask import current_app

from .extensions import db


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


def process_query(query, params):
    result = []

    try:
        current_app.logger.debug(
            "Executing query: %s",
            QueryFiller(query, params),
        )
        data = db.session.execute(query, params)
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as exc:
        full_query = _fill_query(query, params)
        raise Exception(f"Failed to execute query: {full_query}") from exc

    try:
        for row in data:
            result.append(dict(row))
    except sqlalchemy.exc.ResourceClosedError:  # in case of inserting - no rows
        pass

    return result
