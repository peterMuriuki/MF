""" 
users class template : Models the fields and behaviours expected of a user
"""
from flask import current_app
from . import db
from sqlalchemy.exc import OperationalError
from werkzeug.security import generate_password_hash
from marshmallow import fields, Schema, post_load
import os

class Users(db.Model):
    __table_name__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))
    user_name = db.Column(db.String(40))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    admin = db.Column(db.Boolean())

    def __init__(self, name, user_name, email, password, admin=False):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.admin = admin
        self.user_name = user_name

    def __repr__(self):
        """__repr__"""
        return "<user{} {} {} {}>".format(self.id, self.user_name, self.email, self.admin)

    @staticmethod
    def insert_test_admin():
        """ add the super user admin"""
        db.drop_all()
        db.create_all()
        app = current_app._get_current_object()
        name = app.config['EANMBLE_ADMIN_NAME']
        email = app.config['EANMBLE_ADMIN_EMAIL']
        password = app.config['EANMBLE_ADMIN_PASSWORD']
        user_name = app.config['EANMBLE_ADMIN_USER_NAME']
        admin = True
        admin = Users(name = name, user_name=user_name, email=email, password=password, admin=admin)
        try:
            db.session.add(admin)
            db.session.commit()
        except OperationalError as e:
            db.session.rollback()
            return False
        return True

    @staticmethod
    def insert_admin():
        """Add a test super user account"""
        db.drop_all()
        db.create_all()
        name = os.environ.get('EANMBLE_ADMIN_NAME')
        email = os.environ.get('EANMBLE_ADMIN_EMAIL')
        password = os.environ.get('EANMBLE_ADMIN_PASSWORD')
        user_name = os.environ.get('EANMBLE_ADMIN_USER_NAME')
        admin = True
        admin = Users(name = name, user_name=user_name, email=email, password=password, admin=admin)
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
    admin = fields.Boolean()

    @post_load
    def make_user(self, data):
        return Users(**data)