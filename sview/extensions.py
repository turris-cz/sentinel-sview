from flask_babel import Babel
from flask_caching import Cache
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_rq2 import RQ

from .extension_influx import InfluxDB


babel = Babel()
cache = Cache()
influx = InfluxDB()
mail = Mail()
db = SQLAlchemy()
migrate = Migrate(db=db)
redis = FlaskRedis()
rq = RQ()
