""" declare the application factory (create_app method)"""
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
from flask import Flask
from config import config
from .main import main
from .admin import admin


mail = Mail()
moment = Moment()
db = SQLAlchemy()

def create_app(configuration_name):
    app = Flask(__name__)
    configuration_list = ['development', 'testing', 'production', 'default']
    if configuration_name not in configuration_list:
        raise ValueError('Unknown configuration argument')
    app.config.from_object(config[configuration_name])
    config[configuration_name].init_app(app)

    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(admin, url_prefix='/admin/')

    return app