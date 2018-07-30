"""
This module abstracts user functions and separates them from normal tipster actions such as those
in the main blueprint
"""
from flask import Blueprint

user = Blueprint('user', __name__)

from sqlalchemy.exc import OperationalError
from flask import request, make_response, jsonify, current_app
import jwt
import datetime as dt
from werkzeug.security import check_password_hash
from flask_restful import Resource, Api
from ..models import Tipster, Users, UsersSchema
from functools import wraps


# a few gloabls 
tipster = Tipster()
api = Api(user)
userschema = UsersSchema(many=True)
user_schema = UsersSchema()


def token_required(f):
    @wraps(f)
    def decorated(self, *args, **kwargs):
        """
        returns an instance of the user class else returns a None object if the user is not found
        """
        app = current_app._get_current_object()
        key = app.config['SECRET_KEY']
        token = False
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return {'message': 'Token is missing'}, 401
        person = None
        try:
            data = jwt.decode(token, key)
            person = Users.query.filter_by(id=data['user_id']).first()
        except OperationalError:
            return {'message': 'Token is invalid'}, 401
        if person is None:
            return {'message': 'Token is invalid'}, 401
        return f(self, person, *args, **kwargs)
    return decorated


def admin_eyes(f):
    @wraps(f)
    def decorated(self, *args, **kwargs):
        """
        returns an instance of the user class else returns a None object if the user is not found
        """
        app = current_app._get_current_object()
        key = app.config['SECRET_KEY']
        token = False
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return {'message': 'Token is missing'}, 401
        person = None
        try:
            data = jwt.decode(token, key)
            person = Users.query.filter_by(id=data['user_id']).first()
        except:
            return {'message': 'Token is invalid'}, 401
        if person is None:
            return {'message': 'Token is invalid'}, 401
        if person.admin:
            return f(self, *args, **kwargs)
        return {'message': 'User is forbidden'}, 403
    return decorated


def login_failed(message):
    return {'message': '{}'.format(message)
            }, 401


class User(Resource):
    """
    Functions:
    -> Register: -> post details to create an account
    -> login -> post account login credentials to have access to a security token
    -> edit -> to update a user's profile(put operations)
    -> admin tasks:
        -> get a list of all users
        -> delete users
        -> promote users to admin
    """


class Register(User):
    """supports methods for registering users, deleting accounts"""
    def post(self):
        """
        creating a new user account instance
                    INPUT
        "name": "<name>",
        "email": "<email>",
        "user_name": "<user_name>",
        "password": "<password>"

        :returns: json object with fields: id, name, user_name,... check documentation
        """
        data = request.get_json()
        try:
            user = tipster.add_sharp(data)
        except KeyError:
            return {'message': 'error with the keys', 'sample':
                {
                    "name": "<name>",
                    "email": "<email>",
                    "user_name": "<user_name>",
                    "password": "<password>"
                }}, 400
        if user:
            return {'message': "User account created succesfully",
                    'user': user_schema.dump(user).data
            }, 201



class Many(User):
    """ supports get only-> returns a list of all the users and their details"""
    @token_required
    @admin_eyes
    def get(self, current_user):
        """classified admin eyes only
        returns a list of all the users in the system"""
        users = Users.query.all()
        semi_list = list()
        for user in users:
            semi_list.append(user)

        response = userschema.dump(semi_list)
        diction_data = response.data
        return {'users': diction_data}

api.add_resource(Many, '/')


class Single(User):
    """ Returns a single instance of a user"""
    @token_required
    def get(self, current_user, user_id):
        """classified owner's eyes only"""
        if current_user.id != user_id:
            # check that the logged in user is the same as the one authenticated
            return {'message': 'Method not allowed'}, 405
        user = Users.query.filter_by(id=user_id).first()
        if not user:
            return {'message': 'user not found'}, 404
        userschema = UsersSchema()
        schemaobject = userschema.dump(user)
        return {'users': schemaobject.data}


api.add_resource(Single, '/<int:user_id>')

class Login(User):
    """authenticate a person and return a token for future authentications
    input: an accounts credentials: username and Password
    output: a serialized token string"""
    
    def post(self):
        auth = request.authorization
        app = current_app._get_current_object()
        key = app.config['SECRET_KEY']

        if auth:
            if not auth.username or not auth.password:
                return login_failed('The auth object is present but problematic')
            user = Users.query.filter_by(user_name=auth.username).first()
            user_name = auth.username
            password = auth.password
        else:
            # retrieve the authorisation data as json
            response = request.get_json()
            user_name = response['user_name']
            password = response['password']
            user = Users.query.filter_by(user_name=user_name).first()
        if not user:
            return login_failed('The user with the username was not found')
        if check_password_hash(user.password, password):
            if not user.admin:
                token = jwt.encode({'user_id': user.id, 'exp': dt.datetime.utcnow() + dt.timedelta(hours=24)}, key)
            else:
                token = jwt.encode({'user_id': user.id}, key)
            return jsonify({'token': token.decode("UTF-8"), 'admin': user.admin})
        return login_failed('Password does not match {}'.format(password))


class RERegister(User):
    @token_required
    def put(self, user, user_id):
        """Modification of an existing account instance by the account owner"""
        current_user = Users.query.filter_by(id=user_id).first()
        # what if the current user is of a non_existent person-> implies None
        if current_user is None:
            return {"message": "Bad request, the user whose data is to be modified was not found"}, 400
        if user.admin:
            # means we are promoting user
            if not current_user.admin:
                data = {
                    "admin": True
                }
                tipster.modify_sharp(data, current_user)
                return {'message': 'user successfully modified',
                    'user': user_schema.dump(current_user).data
                    }
            else:
                data = {
                    "admin": False
                }
                tipster.modify_sharp(data, current_user)
                return {
                    'message': 'user succesfully modified',
                    'user': user_schema.dump(current_user).data
                    }
        elif user.id != current_user.id:
            return {'message': 'Method not allowed'}, 405
        elif user.id == current_user.id:
            # shows that we are dealing with the same person, simply the user is trying to modify his/her own account
            data = request.get_json()
            response_obj = tipster.modify_sharp(data, user)

            if response_obj:
                return {'message': 'user successfully modified',
                        'user': user_schema.dump(response_obj).data
                        }
            else:
                return {'message': 'error with the keys', 'sample':
                    {
                        "name": "<name>",
                        "email": "<email>",
                        "user_name": "<user_name>",
                        "password": "<password>",
                        "plan": "<plan>"
                    }}, 304

    @token_required
    def delete(self, user, user_id):
        """admin_eyes and accounts owner eyes only"""
        current_user = Users.query.filter_by(id=user_id).first()
        if user.id == current_user.id or user.admin:
            done = tipster.delete_sharp(user)
            if done:
                return {'message': 'Account deleted successfully'}
            else:
                return {'message': 'Account not deleted'}, 304
        else:
            return {'message': 'Method not allowed'}, 403

api.add_resource(Register, '/register')
api.add_resource(RERegister, '/<int:user_id>')
api.add_resource(Login, '/login')
