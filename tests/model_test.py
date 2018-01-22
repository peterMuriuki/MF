import pytest
import json as j_son
from flask import json, url_for
from . import Users, create_app, db, Predictions, Tipster


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


# def test_predictions():  -> requires mock patching
#     """folow up on the above tests:
#     registration -> login -> and now viewing the predictions"""
#     response = client.get(url_for('main.tips'), headers={'x-access-token':token})
#     assert response.status_code == 200
#     data = json.loads(response.data)

def test_user_model_modification():
    """Checks that a users data can be modified as supposed to"""
    # add two random normal user accounts and one more super user account
    user_one_data = {
        "name": "Uhuru Kenyatta",
        "email": "uhunye@gmail.com",
        "user_name": "uhunye",
        "password": "adasdwe"
    }
    user_two_data = {
        "name": "Raila Omolo odinga",
        "email": "cord@gmail.com",
        "user_name": "rao",
        "password": "adasdwe"
    }
    # we will load the super user account variables from the configuration object since they have already been loaded,
    # after setting rhe configuration to testing
    Users.insert_test_admin()
    # now we register the two standard user accounts
    response = client.post(url_for('user.register'), data=j_son.dumps(user_one_data), headers=headers)
    assert(response.status_code == 201)
    first_user_id = json.loads(response.data)['user']['id']
    response = client.post(url_for('user.register'), data=j_son.dumps(user_two_data), headers=headers)
    assert(response.status_code == 201)
    second_user_id = json.loads(response.data)['user']['id']
    # now we login the super user account and use their token credentials to modify the users data(admin property only)
    # . we will also login as one of the users and test that they too can modify their own credentials
    login_data = {
        "user_name": "CAPTAINPRICE",
        "password": "AD ARGA ADADSFA"
    }
    response = client.post(url_for('user.login'), data=j_son.dumps(login_data), headers=headers)
    assert(response.status_code == 200)
    data  = json.loads(response.data)
    token = data['token']
    headers['x-access-token'] = token
    # now we can try modifying a user account credentials -> the admin trying to make another standard user an admin
    mod_data = {
        "name": "ODM Kalonzo",
        "email": "kalonzo@gmail.com",
        "user_name": "melon",
        "password": "cord"
    }
    admin_data = {
        "admin": True
    }
    resc = client.put(url_for('user.single', user_id=second_user_id), data=j_son.dumps(admin_data), headers=headers)
    assert resc.status_code == 200
    # now what if a user wanted to modify their own data -> we login first user and see him try to do it
    login_data = {
        "user_name": "uhunye",
        "password": "adasdwe"
    }
    response = client.post(url_for('user.login'), data=j_son.dumps(login_data), headers=headers)
    assert response.status_code == 200
    headers['x-access-token'] = json.loads(response.data)['token']
    response = client.put(url_for('user.single', user_id=second_user_id), data=j_son.dumps(mod_data), headers=headers)
    assert response.status_code == 405
    response = client.put(url_for('user.single', user_id=first_user_id), data=j_son.dumps(mod_data), headers=headers)
    assert response.status_code == 200
    # check that first user cannot login with the original details anymore
    response = client.post(url_for('user.login'), data=j_son.dumps(login_data), headers=headers)
    assert response.status_code != 200
    login_data = {
        "user_name": "melon",
        "password": "cord"
    }
    response = client.post(url_for('user.login'), data=j_son.dumps(login_data), headers=headers)
    assert response.status_code == 200


def test_user_by_admin():
    """:goal: to make sure the admin can easily delete a user account, a user can only delete their own account"""
    # add two random normal user accounts and one more super user account
    user_one_data = {
        "name": "kalonzo Musyoka",
        "email": "melon@gmail.com",
        "user_name": "uncle",
        "password": "adasdwe"
    }
    user_two_data = {
        "name": "samoei arap ruto",
        "email": "land@gmail.com",
        "user_name": "hustler",
        "password": "adasdwe"
    }
    # we will load the super user account variables from the configuration object since they have already been loaded,
    # after setting rhe configuration to testing
    Users.insert_test_admin()
    # now we register the two standard user accounts
    response = client.post(url_for('user.register'), data=j_son.dumps(user_one_data), headers=headers)
    assert(response.status_code == 201)
    kalonzo_id = json.loads(response.data)['user']['id']
    response = client.post(url_for('user.register'), data=j_son.dumps(user_two_data), headers=headers)
    assert(response.status_code == 201)
    ruto_id = json.loads(response.data)['user']['id']
    # we know login as one of the standard users and try to delete the other user which should fail
    kalonzo_login_data = {
        "user_name": "uncle",
        "password": "adasdwe"
    }
    response = client.post(url_for('user.login'), data=j_son.dumps(kalonzo_login_data), headers=headers)
    assert response.status_code == 200
    kalonzo_token = json.loads(response.data)['token']
    headers['x-access-token'] = kalonzo_token
    response = client.delete(url_for('user.single', user_id=ruto_id), headers=headers)
    assert response.status_code == 403
    assert json.loads(response.data)['message'] == 'Method not allowed'
    # now what if kalonzo deleted their own account: that should be okay
    response = client.delete(url_for('user.single', user_id=kalonzo_id), headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'Account deleted successfully'
    headers['x-access-token'] = None

    # Now its the administrator time to have some fun deleting users he does not like
    login_data = {
        "user_name": "CAPTAINPRICE",
        "password": "AD ARGA ADADSFA"
    }
    response = client.post(url_for('user.login'), data=j_son.dumps(login_data), headers=headers)
    assert(response.status_code == 200)
    data  = json.loads(response.data)
    token = data['token']
    headers['x-access-token'] = token
    response = client.delete(url_for('user.single', user_id=ruto_id), headers=headers)
    assert response.status_code == 200
    assert json.loads(response.data)['message'] == 'Account deleted successfully'

    # if we now tried logging in the other two standard user accounts, it would return an error message
    response = client.post(url_for('user.login'), data=j_son.dumps(kalonzo_login_data), headers=headers)
    assert response.status_code == 401
