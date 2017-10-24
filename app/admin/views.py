from flask import render_template, redirect, url_for
from . import admin


@admin.route('/me')
def admins_panel():
    from ..models import Predictions, Tipster
    sudo_tipster = Tipster()
    """functions: display scraped games; so far, functionality to approve or disapprove a game"""
    # query  the database ; get response in list form and pass to template for parsing
    response_list = Predictions.query.all()
    print(response_list)
    print(type(response_list))
    return render_template('admin/dashboard.html', predictions = response_list)
