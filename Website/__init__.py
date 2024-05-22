from flask import Flask

from Website import views


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.register_blueprint(views.views, url_prefix="/")
    return app
