import pytest
import json as j_son
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
    global headers
    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
        }

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
        "name": "Peter Denzel",
        "email": "Pmui@gmail.com",
        "user_name": "peter",
        "password": "adasdwe"
    }'''
    # kwani how is one supposed to package a json payload to a post request -> not as from data
        # answer the data payload containing the json data should be added as type str
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


def test_user_instance_from_db():
    """this functions checks that the added instance is inside the database as it should"""
    user = Users.query.filter_by(user_name="peter").first()
    assert(user is not None)
    assert(user.email == "Pmui@gmail.com")
    assert(not user.admin)

def test_login():
    """This function checks that login is as intended """
    data = {
        "user_name": "peter",
        "password": "adasdwe"
    }
    response = client.post(url_for('user.login'), data=j_son.dumps(data), headers=headers)
    assert(response.status_code == 200)
    data  = json.loads(response.data)
    token = data['token']
    global token
    assert(data['token'])
    assert(data['admin'] == False)

def test_predictions():
    """folow up on the above tests:
    registration -> login -> and now viewing the predictions"""
    response = client.get(url_for('main.tips'), headers={'x-access-token':token})
    assert response.status_code == 200
    data = json.loads(response.data)
