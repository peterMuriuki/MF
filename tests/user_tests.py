import pytest
from flask import json, url_for
from . import Users, create_app, db


def setup_module(module):
    """sets these all up for the full module execution"""
    # we define the application instance here now
    app = create_app('testing')
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    client = app.test_client()

def teardown_module(module):
    """close up and clear the database """
    db.session.remove()
    db.drop_all()


def test_registration():
    """works properly  against devoid information and responds with the required info
    test ->  post data"""
    data = {
        "name": "",
        "email": "",
        "user_name": "",
        "password": ""
    }
    response = client.post(url_for('user.register'), data=data) 
    assert(response.status_code == 201)
    data = json.loads(response.data)
    assert(data['message'] == "User account created succesfully")
    assert(data['user'] is dict)

def test_registration_from_db():
    """Test the registration mechanism from the database point of view"""
    users = Users.query.all()
    assert(len(users))

