import os
database_base_uri = os.path.join(os.path.dirname(__file__), 'app', 'static', 'db')
logs_url = os.path.join(os.path.dirname(__file__), 'logs', 'mainlog.log')


class Configuration:
    # general configurations
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'adau fagkfa821b 32bdc^!$@sad'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # general email configuration
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') 
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') 
    MAIL_USE_TLS = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # email to which the application can report to in regard to issues that concern the Admin
    WEBMASTER = os.environ.get('WEBMASTER')
    logconf = {
        "version": 1,
        "disable_existing_loggers" : True,
        "formatters":{
            "simple": {
                'class': 'logging.StreamHandler',
                'format': '%(asctime)s[%(levelname)s] :  %(name)s : %(message)s'
            },
            'typersi':{
                'class': 'logging.FileHandler',
                'format': '%(asctime)s[%(levelname)s] :  %(name)s : %(message)s'
            }
        },
        "handlers": {
            "console": {
                "class": 'logging.StreamHandler',
                "level": 'DEBUG',
                "formatter": 'simple'
                },
            'typersi_logs':{
                'class': 'logging.FileHandler',
                'level': 'INFO',
                'filename': logs_url,
                'mode': 'a',
                'formatter': 'typersi'
            }
        },
        "loggers":{
            "simple_logger":{
                "level": 'DEBUG',
                "handlers": ['console'],
                "propagate": 0
            },
            'typersi_logger':{
                "level": 'INFO',
                "handlers": ['typersi_logs'],
                "propagate": 0
            }
        },
        "root":{
            "level": 'DEBUG',
            "handlers": ['console', 'typersi_logs']
        }
    }

    @staticmethod  
    def init_app(app):
        pass

class MiddleWare(Configuration):
    """define the flask_mail configurations options
    -> The Production Configuration will define its own mail configurations"""
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587

class TeDev(MiddleWare):
    """test variables for creating the test_super_user_account"""
    # the below data is fictional
    EANMBLE_ADMIN_NAME = "CAPTAINPRICE"
    EANMBLE_ADMIN_EMAIL = "EANMBLE@GMAIL.com"
    EANMBLE_ADMIN_PASSWORD = "ADARGAADADSFA"
    EANMBLE_ADMIN_USER_NAME = "CAPTAINPRICE"
    EANMBLE_ADMIN_PHONE_NUMBER = '0225468'


class HerokuConfiguration(Configuration):
    """Different settings for heroku deployable application"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True


class DevelopmentConfiguration(TeDev):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(database_base_uri, 'development.db')
    MAIL_USE_TLS = True


class TestingConfiguration(TeDev):
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
    'default' : DevelopmentConfiguration,
    'heroku': HerokuConfiguration
}
