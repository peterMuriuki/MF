""" Launch Script"""
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand, upgrade
from app import create_app, db
from app.models import Predictions, Users
import os, sys


app = create_app(os.environ.get('CONFIGURATION') or 'default')
manager = Manager(app=app)
migrate = Migrate(app=app, db=db)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(app=app, db=db, Predictions=Predictions, Users=Users)

manager.add_command('shell', Shell(make_context=make_shell_context))

@manager.command
def deploy():
    """Define all the deploy operations once and in a encapsulated manner """
    # create the tables
    
    if os.environ['CONFIGURATION'] == 'production' or os.environ['CONFIGURATION'] == 'heroku':
        Users.insert_admin() # will wok for all application configurations
    else:
        Users.insert_test_admin()

    """
    DEPLOYMENT PROCEDURE
    add admin configuration variables to environment
    push to heroku master
    heroku deploy to construct the database and add the administrators account details
    heroku restart
    """

@manager.command
def destroy():
    # just destroy the tables
    db.drop_all()

if __name__ == '__main__':
    manager.run()
