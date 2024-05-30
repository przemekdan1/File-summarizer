from flask import Flask
from file_summarizer_app.routes.home import home
from file_summarizer_app.routes.upload import upload
from prometheus_client import start_http_server

def create_app(config_class='file_summarizer_app.config.DevelopmentConfig'):
    app = Flask(__name__)
    app.config.from_object(config_class)

    if app.config['ENABLE_PROMETHEUS']:
        start_http_server(app.config['PROMETHEUS_PORT'])
    app.register_blueprint(home)
    app.register_blueprint(upload)

    return app









