import pytest
from flask import json, url_for
from . import Users, create_app, db


def setup_module(module):
    """sets these all up for the full module execution"""
    # we define the application instance here now
    app = create_app('testing')
    app.config['SERVER_NAME'] = "127.0.0.1"
    app_context = app.app_context()
    app_context.push()
    db.create_all()
    global client
    client = app.test_client()

def teardown_module(module):
    """close up and clear the database """
    db.session.remove()
    db.drop_all()


def test_return_urls():
    """Get the home route and see if the contents match """
    response = client.get(url_for('main.default'))
    res = json.loads(response.data)
    assert(type(res) is dict)


def test_registration():
    """works properly  against devoid information and responds with the required info
    test ->  post data"""
    data = '''{
        "name": "Peter",
        "email": "Pmuriuki@gmail.com",
        "user_name": "peter",
        "password": "adasdwe"
    }'''
    # kwani how is one supposed to package a json payload to a post request -> not as from data
        # answer the data payload containing the json data should be added as type str
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
        }
    response = client.post(url_for('user.register'), data=data, headers=headers)
    assert(response.status_code == 201)
    data = json.loads(response.data)
    assert(data['message'] == "User account created succesfully")
    print(data['user'])
    assert(type(data['user']) is dict)

def test_registration_from_db():
    """Test the registration mechanism from the database point of view"""
    users = Users.query.all()
    assert(bool(len(users)))

