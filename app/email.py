"""Eanmble email options:
to admin - > new tips
to all users -> A new approved tip"""
from . import mail
from flask import render_template, current_app
from flask_mail import Message
from threading import Thread

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args=args, kwargs=kwargs)
        thr.start()
    return wrapper

@async
def send_async_email(app, msg):
    """requires an active applcation context and the msg"""
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    msg = Message(subject=subject,sender=sender,recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    app = current_app._get_current_object()
    send_async_email(app, msg)


class ToAdmin(object):
    """Represents all the templates of actions that will require the application to send emails to 
    the adminsistrator
    1 a new subscriber
    2 a new unapproved tip
    3 after the end of the recommended tips -> priority low
    4 an error"""
    def __init__(self):
        pass
    
    def new_subscriber(self, user_obj):
        """Will send the public details of the new user object to the administrator """
        message = """ 
            to Admin,

            you have a new user

            {}, username: {} has just subscribed to Eanmble

            contact him at: {}
            """.format(user_obj.name, user_obj.user_name, user_obj.email)
        subject = "(Hooray)NEW USER"
        html_body = render_template('email/new_user.html', user_obj)
        send_email(subject, app.config['MAIL_USERNAME'], 'FLASKY['WEBMASTER']', message, html_body)
        return True

    def error(self, error_message):
        """Forwards an error message ot administrator"""
        subject = "SHIT"
        send_email(subject, app.config['MAIL_USERNAME'], 'FLASKY['WEBMASTER']', error_message, error_message)
        return True

    def new_prediction(self, predictions):
        """Sends informatoion on newly added tips to the administrator"""
        subject = "NEW TIPS"
        message = ""
        for prediction in predictions:
            message += "{} {} {}\n".format(prediction.ficture, prediction.pick, prediction.odds)
        html_body = render_template('email/new_predictions.html', predictions)
        send_email(subject, app.config['MAIL_USERNAME'], 'wpmuriuki98@gmail.com', message, html_body)
        return True


    def end_of_tip_session(self):
        """
        Pending sends an eamail detailing the results of the advised tips as well as the 
        resultant effect on the bacnkroll
        """
        pass

class ToUser(object):
    """
     Represents the templates of the emails to be sent to notify a subscribed user
    1 after a new prediction
    2 after end of play for the given predictions
    3 as a welcome message
    """
    # a welcome message:
    def welcome_email(self, user_obj):
        """Sends  welcome message to a new subscriber"""
        message = """
        hi {}
            
            Its so great that you decided to get onboard Eanmble_ts predictions site.
        in the following days we hope to grow your bankroll without any hustle.

        Eanmble offers another prediction service that will be coming up soon, Eanmble_sp.
        We will notify you as soon as the service is up and running, in the meanwhile lets make
        some dough.

        yours,
        Eanmble_ts admin
        """.format(user_obj.name)

        html_body = render_template('email/welcome.html')
        subject = "{EANMBLE}Just Saying Hello"
        send_email(subject, app.config['MAIL_USERNAME'], user_obj.email, message, html_body)

    def new_approved(self, email_list, predictions):
        """Emails a list of approved predictions to the emailing list of all users includinf the admin"""
        message = ""
        total_odds = 0.00
        for prediction in predictions:
            message += " {} {} {}\n".format(prediction.fixture, prediction.pick, prediction.odds)
        # we need to include staking information some where in the message

    def end_of_tip_session(self):
        """"""
        pass