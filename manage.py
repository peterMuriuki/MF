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
    db.drop_all()
    db.create_all()
    upgrade()

    # add admin
    """Declare the below imported variables in a py-file named admin and place next to the Manage.py deployment file
    the variables declare data used in initialising the super user account allowing for :

    Hardcode the data or import from environment -> therefore add db to ignore list too
        predictions approval
        deleting predictions
        user account managenent
    """
    from admin import name, user_name, email, password, admin, phone_number, bankroll, plan
    admin = Users(name = name, user_name=user_name, email=email, password=password, admin=admin, phone_number=phone_number, bankroll=bankroll, plan=plan)
    db.session.add(admin)
    db.session.commit()


if __name__ == '__main__':
    manager.run()
