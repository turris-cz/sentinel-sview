from flask import current_app, _app_ctx_stack

import influxdb_client

class InfluxDB():
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_appcontext(self.teardown)

    def connect(self):
        return influxdb_client.InfluxDBClient(
            url = current_app.config["INFLUXDB_URL"],
            token = current_app.config["INFLUXDB_TOKEN"],
            org = current_app.config["INFLUXDB_ORGANIZATION"],
        )

    def teardown(self, exception):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, "influxdb"):
            ctx.influxdb.close()

    @property
    def client(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, "influxdb"):
                ctx.sqlite3_db = self.connect()
            return ctx.sqlite3_db
