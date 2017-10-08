import os
database_uri = os.path.join(os.path.dirname(__name__, 'app', 'static', 'db', 'predictions.db'))


class Configuration:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'adau fagkfa821b 32bdc^!$@sad'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + database_uri

    @staticmethod  
    def init_app(app):
        pass


class DevelopmentConfiguration(Configuration):
    DEBUG = True


class TestingConfiguration(Configuration):
    TESTING = True
    DEBUG = True


class ProductionConfiguration(Configuration):
    pass


config = {
    'development': DevelopmentConfiguration,
    'testing': TestingConfiguration,
    'production': ProductionConfiguration,
    'default' : DevelopmentConfiguration
}