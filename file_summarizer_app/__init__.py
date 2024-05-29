from flask import Flask
from file_summarizer_app.routes.home import home
from file_summarizer_app.routes.upload import upload

def create_app():
    app = Flask(__name__)

    app.register_blueprint(home)
    app.register_blueprint(upload)

    return app









