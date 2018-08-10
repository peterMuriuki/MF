"""  declare the application factory (create_app method)"""
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_moment import Moment
from flask import Flask
from config import config, logconf
import logging
import logging.config

moment = Moment()
db = SQLAlchemy()
ma = Marshmallow()

logging.config.dictConfig(logconf)
tlogger = logging.getLogger('typersi_logger')
slogger = logging.getLogger('simple_logger')


def create_app(configuration_name):
    app = Flask(__name__)
    configuration_list = ['development', 'testing', 'heroku', 'production', 'default']
    if configuration_name not in configuration_list:
        raise ValueError('Unknown configuration argument')
    app.config.from_object(config[configuration_name])
    config[configuration_name].init_app(app)
    slogger.debug("Application instance created")
    
    moment.init_app(app)
    db.init_app(app)
    ma.init_app(app)

    from .main.views import main
    from .admin.views import user
    app.register_blueprint(main)
    app.register_blueprint(user, url_prefix='/users')
    slogger.debug("Blueprints succesfully added")

    return app
