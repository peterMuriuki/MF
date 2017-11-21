"""
Loads a single admin account: This file should never be added to a 
version control system as they contain very sensitive data, 

This commands run from within the deploy function in manage and thus loads the database 
with one user who is the admin.
"""

import os


"""Declare the instance variables for creating a super user """
name = os.environ.get('EANMBLE_ADMIN_NAME')
email = os.environ.get('EANMBLE_ADMIN_EMAIL')
password = os.environ.get('EANMBLE_ADMIN_PASSWORD')
user_name = os.environ.get('EANMBLE_ADMIN_USER_NAME')
admin = True
phone_number = os.environ.get('EANMBLE_ADMIN_PHONE_NUMBER')
bankroll = None
plan = None
