class Config(object):
    DEBUG = False
    TESTING = False
    PROMETHEUS_PORT = 8000
    ENABLE_PROMETHEUS = True

class ProductionConfig(Config):
    PROMETHEUS_PORT = 8080
    ENABLE_PROMETHEUS = True

class DevelopmentConfig(Config):
    DEBUG = True
    PROMETHEUS_PORT = 8000
    ENABLE_PROMETHEUS = True

class TestingConfig(Config):
    TESTING = True
    PROMETHEUS_PORT = 8001
    ENABLE_PROMETHEUS = False
