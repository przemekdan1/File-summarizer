class Config(object):
    DEBUG = False
    TESTING = False
    PROMETHEUS_PORT = 8000  # Default port for Prometheus metrics
    ENABLE_PROMETHEUS = True  # Flag to enable/disable Prometheus metrics

class ProductionConfig(Config):
    PROMETHEUS_PORT = 8080  # Different port in production
    ENABLE_PROMETHEUS = True

class DevelopmentConfig(Config):
    DEBUG = True
    PROMETHEUS_PORT = 8000
    ENABLE_PROMETHEUS = True

class TestingConfig(Config):
    TESTING = True
    PROMETHEUS_PORT = 8001
    ENABLE_PROMETHEUS = False  # Typically disable Prometheus in testing
