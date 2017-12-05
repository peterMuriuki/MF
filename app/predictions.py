"""What a prediction instance looks like"""

from . import db
from marshmallow import fields, Schema, post_load
from datetime import datetime
from sqlalchemy.exc import OperationalError


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
    sport = db.Column(db.String(20), nullable=True)
    count = db.Column(db.Integer(), nullable=True)
    comment= db.Column(db.Text(), nullable=True)

    def __repr__(self):
        """returns/displays an arbitrary representation of a row"""
        return "<Prediction %r %r %r %r %r %r %r %r %r %r>" % (self.id, self.date_time, self.fixture,
     self.tipster_url, self.pick, self.confidence, self.odds, self.approved, self.sport, self.count)

    def __init__(self, prediction_id, fixture, tipster_url, tipster_name, pick,
    confidence, odds, _time=datetime.utcnow(), sport='', approve=False, count=0, home_score=None,
    away_score=None):
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
        self.home_score = home_score
        self.away_score = away_score

    def approve(self):
        """After a prediction is looked up and approved by admin; set confirm to True"""
        self.approved = True
        db.session.commit()

    def set_score(self, home_score, away_score):
        """set the result after full time. asynchronously check the odds"""
        self.home_score = home_score
        self.away_score = away_score
        db.session.commit()

    def add_comment(self, comment):
        """:param: analysis by the admin"""
        try:
            self.comment = comment
            db.session.commit()
        except OperationalError as error:
            db.session.rollback()

class PredictionsSchema(Schema):
    """ defines the schema for serializing and deserializing dictionaries and objects"""
    id = fields.Integer()
    prediction_id = fields.String()
    fixture = fields.String()
    tipster_url = fields.String()
    tipster_name = fields.String()
    date_time = fields.String()
    pick = fields.String()
    confidence = fields.Float()
    odds = fields.Float()
    approved = fields.Boolean()
    sport = fields.String()
    count = fields.Integer()
    comment = fields.String()

    @post_load
    def make_user(self, data):
        return Predictions(**data)