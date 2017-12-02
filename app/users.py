""" 
users class template : Models the fields and behaviours expected of a user
"""
from . import db
from sqlalchemy.exc import OperationalError
from werkzeug.security import generate_password_hash
from marshmallow import fields, Schema, post_load

class Users(db.Model):
    __table_name__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))
    user_name = db.Column(db.String(40))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    phone_number = db.Column(db.String(), nullable=True)
    admin = db.Column(db.Boolean())
    plan = db.Column(db.String(10), nullable=True)
    bankroll = db.Column(db.Float())

    def __init__(self, name, user_name, email, password, admin=False, phone_number=None, bankroll=None, plan=None):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.admin = admin
        self.user_name = user_name

    def __repr__(self):
        """__repr__"""
        return "<user{} {} {} {}".format(self.id, self.user_name, self.email, self.admin)

    def set_plan(self, plan):
        """ Sets the plan as a string represetntations of the class name"""
        self.plan = plan

    def set_bankroll(self, bankroll):
        """called upon once a user decides to credit his acount with cash"""
        self.bankroll = bankroll

    @staticmethod
    def insert_admin():
        """ add the super user admin"""
        name = os.environ.get('EANMBLE_ADMIN_NAME')
        email = os.environ.get('EANMBLE_ADMIN_EMAIL')
        password = os.environ.get('EANMBLE_ADMIN_PASSWORD')
        user_name = os.environ.get('EANMBLE_ADMIN_USER_NAME')
        admin = True
        phone_number = os.environ.get('EANMBLE_ADMIN_PHONE_NUMBER')
        bankroll = None
        plan = None
        admin = Users(name = name, user_name=user_name, email=email, password=password, admin=admin, phone_number=phone_number, bankroll=bankroll, plan=plan)
        try:
            db.session.add(admin)
            db.session.commit()
        except OperationalError as e:
            db.session.rollback()
            return False
        return True


class UsersSchema(Schema):
    """Defines the serialization and deserialization of the users class to and from dict to python object"""
    id = fields.Integer()
    name = fields.String()
    user_name = fields.String()
    email = fields.Email()
    password = fields.String()
    phone_number = fields.Integer()
    admin = fields.Boolean()
    plan = fields.String()
    bankroll = fields.Float()

    @post_load
    def make_user(self, data):
        return Users(**data)