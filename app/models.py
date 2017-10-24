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
    confirmed = db.Column(db.Boolean())
    sport = db.Column(db.String(20))

    def __repr__(self):
        """returns/displays an arbitrary representation of a row"""
        return "<Prediction %r %r %r %r %r %r %r %r %r %r>" % (self.id, self.home_team, self.away_team,
    self.tipster_url, self.tipster_url, self.pick, self.confidence, self.odds, self.confirmed, self.sport)

    def __init__(self, prediction_id, home_team, away_team, tipster_url, tipster_name, pick,
    confidence, odds, sport='', confirmed=False):
        self.prediction_id = prediction_id
        self.home_team = home_team
        self.away_team = away_team
        self.tipster_url = tipster_url
        self.tipster_name = tipster_name
        self.pick = pick
        self.confidence = confidence
        self.odds = odds
        self.confirmed = confirmed
        self.sport = sport

    def confirm(self):
        """After a prediction is looked up abd confirmed by admin; set confirm to True"""
        self.confirmed = True

class Tipster(object):
    """toolboc for all methods and functions for manipulating the predictions"""
    # each method's data transactions should be atomic

    def add_prediction(self, diction):
        """creates a single instance of a prediction and commits it to the database"""
        pred_id, h_t, a_t, t_u, t_n, pick, con, odds = diction['prediction_id'], diction['home_team'], diction['away_team'], diction['tipster_url'], diction['tipster_name'], diction['pick'], diction['confidence'], diction['odds']
        prediction_obj = Predictions(pred_id, h_t, a_t, t_u, t_n, pick, con, odds)
        db.session.add(prediction_obj)
        db.session.commit()

    def confirm_prediction(self, prediction_obj):
        """ calls the confirm method from the parsed in prediction_obj"""
        prediction_obj.confirm()
        return True
