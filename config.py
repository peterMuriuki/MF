import os
database_base_uri = os.path.join(os.path.dirname(__file__), 'app', 'static', 'db')


class Configuration:
    # general configurations
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'adau fagkfa821b 32bdc^!$@sad'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # general email configuration
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or '@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'n/a'

    @staticmethod  
    def init_app(app):
        pass

class MiddleWare(Configuration):
    """define the flask_mail configurations options
    -> The Production Configuration will define its own mail configurations"""
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587


class DevelopmentConfiguration(MiddleWare):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(database_base_uri, 'development.db')


class TestingConfiguration(MiddleWare):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(database_base_uri, 'testing.db')


class ProductionConfiguration(Configuration):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(database_base_uri, 'production.db')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True


config = {
    'development': DevelopmentConfiguration,
    'testing': TestingConfiguration,
    'production': ProductionConfiguration,
    'default' : DevelopmentConfiguration
}
