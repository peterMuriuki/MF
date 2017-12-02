"""
Consolidate the data Model definitions and also add supports for tipster gear functionalities
"""
from . import db
from sqlalchemy.exc import OperationalError
from .users import *
from .predictions import *
from .plan import *
import os


class Tipster(object):
    """toolbox for all methods and functions for manipulating the predictions"""
    # each method's data transactions should be atomic

    def approve_prediction(self, prediction_obj):
        """ calls the confirm method from the parsed in prediction_obj"""
        prediction_obj.approve()
        db.session.commit()
        return prediction_obj

    def get_all_predictions(self):
        """qeuries the Predictions relations for all existent predictions
        output:-> returns them as a dictionary of lists"""
        response = Predictions.query.all()
        return {'predictions': response}

    def add_sharp(self, data):
        """adds a new user to database"""
        name = data['name']
        email = data['email']
        user_name = data['user_name']
        password = data['password']


        user = Users(name=name, user_name=user_name, email=email, password=password)
        try:
            db.session.add(user)
            db.session.commit()
        except OperationalError as e:
            db.session.rollback()
            # do sth here maybe send a fkn email or throw another more manageable error
        return user

    def add_prediction(self, data):
        """add prediction"""
        pred_id = data["prediction_id"]
        fixture = data["fixture"]
        url = data["tipster_url"]
        name = data["tipster_name"]
        pick = data["pick"]
        confidence = data["confidence"]
        odds = data["odds"]
        _time = data['time_of_play']
        count = data['count']
        pred_obj = Predictions(prediction_id=pred_id, _time=_time, fixture=fixture, tipster_url=url, tipster_name=name,
                               pick=pick, confidence=confidence, odds=odds, count=count)
        db.session.add(pred_obj)
        db.session.commit()
        return pred_obj

    def delete_sharp(self, user_obj):
        """remove a user from the database"""
        try:
            db.session.delete(user_obj)
            db.session.commit()
        except OperationalError:
            return False
        return True

    def modify_sharp(self, data, user):
        """Modifies a user credentials"""
        name = data.get('name')
        email = data.get('email')
        user_name = data.get('user_name')
        password = data.get('password')
        plan = data.get('plan')


        if name is not None:
            user.name = name
        if email is not None:
            user.email = email
        if user_name is not None:
            user.user_name = user_name
        if password is not None:
            user.password = password
        if plan is not None:
            user.plan = plan

        db.session.commit()
        return user

    def delete_prediction(self, pred_obj):
        """Removes a prediction object"""
        try:
            db.session.delete(pred_obj)
            db.session.commit()
        except OperationalError as e:
            db.session.rollback()
        return True
