from flask_babel import Babel
from flask_caching import Cache
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from flask_rq2 import RQ


babel = Babel()
cache = Cache()
mail = Mail()
db = SQLAlchemy()
redis = FlaskRedis()
rq = RQ()
