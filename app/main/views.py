"""this modules blueprint view serves to only deal with the predictions endpoint"""
from flask import request, url_for, make_response
from ..admin.views import token_required, Users, admin_eyes
from flask_restful import Resource, Api, fields
from ..models import Tipster, Predictions, PredictionsSchema
from ..scrapper import run
from flask import Blueprint


main = Blueprint('main', __name__)

api = Api(main)
tipster = Tipster()
predschema = PredictionsSchema(many=True)
pred_schema = PredictionsSchema()

# login wrapper method:-> for receiving the security token and returning boolean
# this method only ensures that the routes are protected against anonymous users only
# the admin_only decorator will restrict the view function to admin only.


def default_response():
    return {'urls':
                    {
                        'endpoint' : 'url_ednpoint url',
                        'Predictions': url_for('main.tips', _external=True),
                        'users': url_for('user.many', _external=True),
                        'help': url_for('main.default', _external=True)
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
        pred_obj = Predictions.query.filter_by(id=pred_id).first()
        pred_obj = tipster.approve_prediction(pred_obj)
        return {
                    'message': 'approved {}'.format(pred_id),
                    "prediction": pred_schema.dump(pred_obj).data
                }, 201

    @token_required
    def get(self, current_user, pred_id):
        """Returns a single instance of the prediction
        input: -> prediction id
        output: -> a dictionary containing the single prediction id
        """
        pred_obj = Predictions.query.filter_by(id=pred_id).first()
        if pred_obj is None:
            return {'message': 'prediction not found'}, 404

        return {"message": "Success",
                "prediction": pred_schema.dump(pred_obj).data
                }, 200

    @token_required
    @admin_eyes
    def delete(self, pred_id):
        """removes the prediction instance
        input: -> encoded secret key with the predictions prediction_id
        output: -> message"""
        pred_obj = Predictions.query.filter_by(id=pred_id).first()
        done = tipster.delete_prediction(pred_obj)
        if done:
            return {'message': 'Prediction deleted'}
        else:
            return { "message": "Prediction Not modified"}, 304

    
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
        try:
            pred_obj = tipster.add_prediction(data)
        except:
            return {"prediction_id": "", "fixture":"", "tipster_url":"", "tipster_name":"", "pick":"",
                "confidence": "", "odds": ""}, 304
        return {'message': 'Prediction created successfully',
                "prediction": pred_schema.dump(pred_obj).data}, 201

    @token_required
    def get(self, current_user):
        """ returns a list of the current predictions of the current day, during test return all predictions
        input: -> nothing
        output: -> a dictionary of lists with the key prediction. the list conatains dictionaries representing predictions instances
        """
        # run scrapper before the predictions are returned otherwise the predictions returned will not include the latest updates
        run()
        from datetime import date as dt
        from datetime import datetime as cal
        date = dt.today()
        today = cal(date.year, date.month, date.day, 0, 0, 0)
        # so that we can only get the predictions whose added time is greater than the start of the day.
        predictions = Predictions.query.filter_by(date_time >= today).all()
        list_ = []
        for prediction in predictions:
            list_.append(prediction)
        result = predschema.dump(list_)
        return {'predictions': result.data}



api.add_resource(Tips_id, '/predictions/<string:pred_id>' )
api.add_resource(Tips, '/predictions/')
