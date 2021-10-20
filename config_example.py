class Config(object):
    DEBUG = False
    TESTING = False

class ProductionConfig(Config):
    POSTGRES_HOSTNAME = "postgres"
    POSTGRES_DB = "pwned"
    POSTGRES_USER = ""
    POSTGRES_PASSWORD = ""

class DevelopmentConfig(Config):
    POSTGRES_HOSTNAME = "127.0.0.1"
    POSTGRES_DB = "pwned-test"
    POSTGRES_USER = "pwned-user"
    POSTGRES_PASSWORD = "pwned-secret"

    DEBUG = True

class TestingConfig(Config):
    TESTING = True