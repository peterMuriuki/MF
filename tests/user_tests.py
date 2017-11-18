import pytest
from flask import json


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


def test_registration(self):
    """works properly  against devoid information and responds with the required info
    test ->  post data"""
    data = {
        "name": "",
        "email": "",
        "user_name": "",
        "password": ""
    }
    response = client.post(, data=data)  # how the fuck am i going to work with routes when i have abstracted taht part of the code to flask-restful
    assert(response.status_code == 201)
    data = json.loads(response.data)
    assert(data['message'] == "User account created succesfully"])
    assert(data['user'] is dict)

