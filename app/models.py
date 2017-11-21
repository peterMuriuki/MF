"""Model the database relationships for data persistence"""
from . import db
from werkzeug.security import generate_password_hash
from marshmallow import fields, Schema, post_load
from datetime import datetime


class Predictions(db.Model):
    __table_name__ = "predictions"
    id = db.Column(db.Integer(), primary_key=True)
    prediction_id = db.Column(db.String(), unique=True)
    date_time = db.Column(db.DateTime(), nullable=False, default=datetime.utcnow)
    fixture = db.Column(db.String(100))
    tipster_url = db.Column(db.String(64))
    tipster_name = db.Column(db.String(64))
    pick = db.Column(db.String(5))
    confidence = db.Column(db.Float())
    odds = db.Column(db.Float())
    approved = db.Column(db.Boolean())
    home_score = db.Column(db.Integer(), nullable=True)
    away_score = db.Column(db.Integer(), nullable=True)
    sport = db.Column(db.String(20))
    count = db.Column(db.Integer(), nullable=True)

    def __repr__(self):
        """returns/displays an arbitrary representation of a row"""
        return "<Prediction %r %r %r %r %r %r %r %r %r %r>" % (self.id, self.date_time, self.fixture,
     self.tipster_url, self.pick, self.confidence, self.odds, self.approved, self.sport, self.count)

    def __init__(self, prediction_id, fixture, tipster_url, tipster_name, pick,
    confidence, odds, _time=datetime.utcnow(), sport='', approve=False, count=0):
        self.prediction_id = prediction_id
        self.fixture = fixture
        self.date_time = _time
        self.tipster_url = tipster_url
        self.tipster_name = tipster_name
        self.pick = pick
        self.confidence = confidence
        self.odds = odds
        self.approved = approve
        self.sport = sport
        self.count = count

    def approve(self):
        """After a prediction is looked up and approved by admin; set confirm to True"""
        self.approved = True

    def set_score(self, home_score, away_score):
        """set the result after full time. asynchronously check the odds"""
        self.home_score = home_score
        self.away_score = away_score

class PredictionsSchema(Schema):
    """ defines the schema for serializing and deserializing dictionaries and objects"""
    id = fields.Integer()
    prediction_id = fields.String()
    fixture = fields.String()
    tipster_url = fields.String()
	# date_time = fields.string()
    pick = fields.String()
    confidence = fields.Float()
    odds = fields.Float()
    approved = fields.Boolean()
    sport = fields.String()
    count = fields.Integer()

    @post_load
    def make_user(self, data):
        return Predictions(**data)

class Users(db.Model):
    __table_name__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))
    user_name = db.Column(db.String(40))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    phone_number = db.Column(db.String(), nullable=True)
    admin = db.Column(db.Boolean())
    plan = db.Column(db.String(10), nullable=True)
    bankroll = db.Column(db.Float())
    
    def __init__(self, name, user_name, email, password, admin=False, phone_number=None, bankroll=None, plan=None):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password)
        self.admin = admin
        self.user_name = user_name

    def set_plan(self, plan):
        """ Sets the plan as a string represetntations of the class name"""
        self.plan = plan

    def set_bankroll(self, bankroll):
        """called upon once a user decides to credit his acount with cash"""
        self.bankroll = bankroll

class UsersSchema(Schema):
    """Defines the serialization and deserialization of the users class to and from dict to python object"""
    id = fields.Integer()
    name = fields.String()
    user_name = fields.String()
    email = fields.Email()
    password = fields.String()
    phone_number = fields.Integer()
    admin = fields.Boolean()
    plan = fields.String()
    bankroll =fields.Float()

    @post_load
    def make_user(self, data):
        return Users(**data)

class Tipster(object):
    """toolboc for all methods and functions for manipulating the predictions"""
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
        db.session.add(user)
        db.session.commit()
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
        except:
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
        db.session.delete(pred_obj)
        db.session.commit()
        return True

class Plans(object):
    """the base class that models all the other plans"""

    def __init__(self):
        bank_balance = 0.00

    def get_stake(self):
        """ to be overriden in the different plans"""

    def update_bank_balance(self):
        """Also to be overriden """

    def place_bet(self):
        """
        will be responsible for consolidating all the required functions for 
        bet placement, bet settlement and bankroll modification
        """



class TrippleOrNothing(Plans):
    """this plan; you stake all on an odd of three"""

    def __init__(self):
        super().__init__()

    def get_stake(self):
        return self.bank_balance

    def update_bank_balance(self, odds=None):
        pass


class DoubleOrNothing(Plans):
    """ all money back on double odds."""
