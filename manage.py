""" Launch Script"""
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand, upgrade
from app import create_app, db
from app.models import Predictions, Users
import os


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
    upgrade()


if __name__ == '__main__':
    manager.run()
