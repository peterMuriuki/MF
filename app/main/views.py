from flask import request, url_for, make_response, jsonify
import datetime, os
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from werkzeug.security import check_password_hash
from flask_restful import Resource, Api
from . import main
from ..models import Tipster, Users
from manage import app
from ..scrapper import run
from functools import wraps

api = Api(main)
tipster = Tipster()

# login wrapper method:-> for receiving the security token and returning boolean
# this method only ensures that the routes are protected against anonymous users only
# the admin_only decorator will return true or false based on whether the current user is an admin



class Default(Resource):
    """This class contains support for the default route '/'"""

    def get(self):
        """return the correct urls and sample"""
        return {'urls': [
            {
                'message': 'get a single Prediction instance',
                'get_url_sample': ''
            },
            {
                'message': 'get all predictions',
                'get_url_sample': ''
            }
        ]}

    def post(self):
        """There is some controversy on whether i should allow this method or even if
        this method should have been created in the first place."""
        return make_response({'message': 'method not allowed for now'}, 503)

    def put(self):
        """displays the allowed urls for activating a prediction"""
        return {'message': 'classified admin eyes only',
                'put_url_sample': ''}

    def delete(self):
        """admin eyes only too"""
        return {'message': 'classified admin eyes only',
                'delete_url_sample': ''}

api.add_resource(Default, '/')

class Tips_id(Resource):
    """Endpoint Resource:
    get -> return a single prediction
    post -> add predictions to the database
    put -> approve confirmation/ classified admin eyes only
    delete -> remove a prediction from any level of consideration
    """
    def put(self, pred_id):
        """ updates the approved boolean property of the prediction
        input: -> the Prediction's prediction_key from decoded secret key
        output: -> message; and object details"""
        return {'message': 'approved {}'.format(pred_id)}

    @token_required
    def get(self, current_user, pred_id):
        """Returns a single instance of the prediction
        input: -> prediction id
        output: -> a dictionary containing the single prediction id
        """
        if not current_user:
            return {'message': 'Authorization error, please recheck your token'}
        return {'message': 'returned {} only'.format(pred_id)}

    def delete(self, pred_id):
        """removes the prediction instance
        input: -> encoded secret key with the predictions prediction_id
        output: -> message"""
        return {'message': 'Prediction deleted'}

    
class Tips(Resource):
    """Endpoint Resource:
    get -> return all saved predictions for the day
    post -> add predictions to the database
    """
    def post(self):
        """add a new prediction
        input: -> diction from scrapped data
        output -> urls for the created resource; serialized object"""
        data = request.get_json()
        return {'message': 'just added '}

    @token_required
    def get(self, current_user):
        """ returns a list of the current predictions of the current day, during test return all predictions
        input: -> nothing
        output: -> a dictionary of lists"""
        if not current_user:
            return {'message': 'Authorization error, please recheck your token'}
        run()
        return {'message': 'returned all'}



api.add_resource(Tips_id, '/predictions/<string:pred_id>')
api.add_resource(Tips, '/predictions/')
