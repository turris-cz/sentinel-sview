class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    DB_NAME = ""
    DB_USERNAME = ""


class DevelopmentConfig(Config):
    DB_HOSTNAME = "127.0.0.1"
    DB_NAME = "hapi"
    DB_USERNAME = "hapi_user"
    DB_PASSWORD = "hapi-secret"

    DEBUG = True

class TestingConfig(Config):
    TESTING = True