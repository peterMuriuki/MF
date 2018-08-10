"""Eanmble email options:
to admin - > new tips
to all users -> A new approved tip"""
from . import tlogger, slogger
from flask import render_template, current_app
import os, requests

domain = "https://api.mailgun.net/v3/sandbox634d51bb58174800abf3e2c0f562b31e.mailgun.org/messages"
api_key = os.environ.get('MAIL_GUN_API')
if not api_key:
    raise Exception('The mail gun api-key is not set')

def send_email(subject, sender, recipients, text_body, html_body):
    return requests.post(
        domain,
        auth=("api", api_key),
        data={"from": "Mailgun Sandbox <postmaster@sandbox634d51bb58174800abf3e2c0f562b31e.mailgun.org>",
              "to": recipients,
              "subject": subject,
              "text": text_body})


class ToAdmin(object):
    """Represents all the templates of actions that will require the application to send emails to 
    the administrator
    2 new unapproved tips
    3. new subscriptions
    4 an error"""

    @staticmethod
    def new_subscriber(user_obj):
        """Will send the public details of the new user object to the administrator """
        message = """ 
            to Admin,

            you have a new user

            {}, username: {} has just subscribed to Eanmble

            contact him at: {}
            """.format(user_obj.name, user_obj.user_name, user_obj.email)
        app = current_app._get_current_object()
        subject = "(Hooray)NEW USER"
        html_body = render_template('email/new_user.html', user_obj = user_obj)
        return send_email(subject, app.config['MAIL_USERNAME'], [app.config['WEBMASTER']], message, html_body)
        

    @staticmethod
    def error(domain_of_error, error_message):
        """Forwards an error message to administrator"""
        subject = domain_of_error
        app = current_app._get_current_object()
        return send_email(subject, app.config['MAIL_USERNAME'], [app.config['WEBMASTER']], error_message, '')
        

    @staticmethod
    def new_prediction(predictions):
        """Sends information on newly added tips to the administrator
        :param: a list of dictionaries"""
        subject = "NEW TIPS"
        message = ""
        app = current_app._get_current_object()
        for prediction in predictions:
            message += "{} {} {}\n".format(prediction['fixture'], prediction['pick'], str(prediction['odds']))
        html_body = render_template('email/new_predictions.html', predictions = predictions)
        return send_email(subject, app.config['MAIL_USERNAME'], [app.config['WEBMASTER']], message, html_body)
        
class ToUser(object):
    """welcome message """
    
    @staticmethod
    def welcome(user_object):
        """"""
        subject = "Saying Hello"
        html_body = render_template('email/welcome.html', user_object=user_object)
        message = """
            hi {}
                Its so great that you decided to get on-board Eanmble_ts predictions site.
                in the following days we hope to grow your bankroll without any hustle.

                Eanmble offers another prediction service that will be coming up soon, Eanmble_sp.
                We will notify you as soon as the service is up and running, in the meanwhile lets make
                some dough.

                yours,
                Eanmble_ts admin""".format(user_object.name)
        return send_email(subject, '', user_object.email, message, html_body)