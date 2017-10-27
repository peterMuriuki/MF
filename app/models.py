"""Model the database relationships for data persistence"""
from . import db

class Predictions(db.Model):
    __table_name__ = "predictions"
    id = db.Column(db.Integer(), primary_key=True)
    prediction_id = db.Column(db.String(), unique=True)
    home_team = db.Column(db.String(64))
    away_team = db.Column(db.String(64))
    tipster_url = db.Column(db.String(64))
    tipster_name = db.Column(db.String(64))
    pick = db.Column(db.String(5))
    confidence = db.Column(db.Float())
    odds = db.Column(db.Float())
    approved = db.Column(db.Boolean())
    home_score = db.Column(db.integer(), nullable=True)
    away_score = db.Column(db.Integer(), nullable=True)
    sport = db.Column(db.String(20))

    def __repr__(self):
        """returns/displays an arbitrary representation of a row"""
        return "<Prediction %r %r %r %r %r %r %r %r %r %r>" % (self.id, self.home_team, self.away_team,
    self.tipster_url, self.tipster_url, self.pick, self.confidence, self.odds, self.approved, self.sport)

    def __init__(self, prediction_id, home_team, away_team, tipster_url, tipster_name, pick,
    confidence, odds, sport='', approve=False):
        self.prediction_id = prediction_id
        self.home_team = home_team
        self.away_team = away_team
        self.tipster_url = tipster_url
        self.tipster_name = tipster_name
        self.pick = pick
        self.confidence = confidence
        self.odds = odds
        self.approved = approve
        self.sport = sport

    def approve(self):
        """After a prediction is looked up and approved by admin; set confirm to True"""
        self.approved = True

    def set_score(self, home_score, away_score):
        """set the result after full time. asynchronously check the odds"""
        self.home_score = home_score
        self.away_score = away_score

class Users(db.Model):
    __table_name__ = "users"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))
    phone_number = db.Column(db.Iinteger(), nullable=True)
    admin = db.Column(db.Boolean())
    
    def __init__(self, name, email, phone, password, admin=False):
        self.name = name
        self.email = email
        self.phone_number = phone
        self.password = password
        self.admin = admin

class Tipster(object):
    """toolboc for all methods and functions for manipulating the predictions"""
    # each method's data transactions should be atomic

    def add_prediction(self, diction):
        """creates a single instance of a prediction and commits it to the database"""
        pred_id, h_t, a_t, t_u, t_n, pick, con, odds = diction['prediction_id'], diction['home_team'], diction['away_team'], diction['tipster_url'], diction['tipster_name'], diction['pick'], diction['confidence'], diction['odds']
        prediction_obj = Predictions(pred_id, h_t, a_t, t_u, t_n, pick, con, odds)
        db.session.add(prediction_obj)
        db.session.commit()

    def approve_prediction(self, prediction_obj):
        """ calls the confirm method from the parsed in prediction_obj"""
        prediction_obj.approve()
        return True

    def get_all_predictions(self):
        """qeuries the Predictions relations for all existent predictions
        output:-> returns them as a dictionary of lists"""
        response = Predictions.query.all()
        return {'predictions': response}


class Plans(object):
    """the base class that models all the other plans"""

    def __init__(self):
        bank_balance = 0.00

    def get_stake(self):
        """ to be overriden in the different plans"""

    def update_bank_balance(self):
        """Also to be overriden """


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
