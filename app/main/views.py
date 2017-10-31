"""this modules blueprint view serves to only deal with the predictions endpoint"""
from flask import request, url_for, make_response
from ..admin.views import token_required, Users, admin_eyes
from flask_restful import Resource, Api
from . import main
from ..models import Tipster, Predictions, PredictionsSchema
from ..scrapper import run


api = Api(main)
tipster = Tipster()
predschema = PredictionsSchema(many=True)

# login wrapper method:-> for receiving the security token and returning boolean
# this method only ensures that the routes are protected against anonymous users only
# the admin_only decorator will return true or false based on whether the current user is an admin


def default_response():
    return {'urls':
                    {
                        'endpoint' : 'url_ednpoint'
                        # 'Predictions': url_for(Tips, _external=True),
                        # 'users': url_for(Users, _external=True),
                        # 'help': url_for(Default, _external=True)
                    }
            }


class Default(Resource):
    """This class contains support for the default route '/'"""

    def get(self):
        """return the correct urls and sample"""
        return default_response()

    def post(self):
        """There is some controversy on whether i should allow this method or even if
        this method should have been created in the first place."""
        return default_response()

    def put(self):
        """displays the allowed urls for activating a prediction"""
        return default_response()

    def delete(self):
        """admin eyes only too"""
        return default_response()

api.add_resource(Default, '/')

class Tips_id(Resource):
    """Endpoint Resource:
    get -> return a single prediction
    post -> add predictions to the database
    put -> approve confirmation/ classified admin eyes only
    delete -> remove a prediction from any level of consideration
    """
    @token_required
    @admin_eyes
    def put(self, current_user, pred_id):
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
        return {'message': 'returned {} only'.format(pred_id)}

    @token_required
    @admin_eyes
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
    @token_required
    @admin_eyes
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
        # run()
        predictions = Predictions.query.all()
        list_ = []
        for prediction in predictions:
            list_.append(prediction)
        run()
        result = predschema.dump(list_)
        return {'predictions': result.data}



api.add_resource(Tips_id, '/predictions/<string:pred_id>')
api.add_resource(Tips, '/predictions/')
