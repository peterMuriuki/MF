"""  declare the application factory (create_app method)"""
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_mail import Mail
from flask_moment import Moment
from flask import Flask
from config import config


mail = Mail()
moment = Moment()
db = SQLAlchemy()
ma = Marshmallow()


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
    ma.init_app(app)

    from .main import main
    from .admin import user
    app.register_blueprint(main)
    app.register_blueprint(user, url_prefix='/users')

    return app
