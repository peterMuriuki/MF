"""Test file"""
import os
import pytest
from . import *
from bs4 import BeautifulSoup


base_url = os.path.dirname(__file__)
golden_files = os.path.abspath(os.path.join(os.path.dirname(base_url), 'files'))
home_golden_files = os.path.join(golden_files, 'home')
rem_golden_files = os.path.join(golden_files, 'remainder')
home_files_list = os.listdir(home_golden_files)
rem_files_list = os.listdir(rem_golden_files)
re_abs_files = [os.path.abspath(os.path.join(rem_golden_files, file)) for file in rem_files_list]
asb_files = [os.path.abspath(os.path.join(home_golden_files, file)) for file in home_files_list]

def setup_module(module):
    """sets these all up for the full module execution"""
    # we define the application instance here now
    app = create_app('testing')
    app_context = app.app_context()
    app_context.push()
    db.create_all()

def teardown_module(module):
    """close up and clear the database """
    db.session.remove()
    db.drop_all()


@pytest.mark.parametrize('file',asb_files)
def test_full_scrapper(file):
    """See what errors will be thrown or what will not work"""
    # run the command for each file, each time clearing the database
    soup  = get_home_page(file=file)
    response = get_picks_from_tipsters_with_the_best_efficiency(soup)
    assert type(response) is dict
    assert type(soup) is BeautifulSoup

@pytest.mark.parametrize('file', re_abs_files)
def test_remainder_pages_scrapper(file):
    """SEcond scrap functionality: the one that relies on count"""
    response = get_all_other_tips(file=file)
    assert type(response) is dict

def test_predictions_fields_with_count():
    """assert that there are predictions that have the count"""
    response = Predictions.query.all()
        
    # response = Predictions.query.filter_by(count>2).all()
    # assert len(response) > 0


