"""Test file"""
import os
import pytest
from . import create_app, Predictions, Users, Tipster, db, get_all_other_tips, get_home_page, get_picks_from_tipsters_with_the_best_efficiency
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
    tipster = Tipster()
    global tipster
    db.drop_all()
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
    """Second scrap functionality: the one that relies on count"""
    response = get_all_other_tips(file=file)
    assert type(response) is dict

def test_predictions_fields_with_count():
    """assert that there are predictions that have the count"""
    response = Predictions.query.all()    
    response = Predictions.query.filter(Predictions.count >= 2).all()
    assert len(response) > 0


def test_modify_predictions_standard_case():
    """ checks that given a proper json dictionary object; the tipster is able to correctly
    change only the defined data members of the respective project
    """
    data = {
        "approved": 2,
        "home_score": 20,
        "away_score": 30,
        "comment": "this is the Super user comment"
    }
    pred = Predictions.query.filter_by(id=1).first()
    assert not pred.approved
    assert pred.home_score != 20
    assert pred.away_score != 30
    assert pred.comment is None
    mod = tipster.modify_prediction(data, pred)
    assert mod.id == 1
    assert mod.approved == 2
    assert mod.home_score == 20
    assert mod.away_score == 30
    assert mod.comment == "this is the Super user comment"


def test_modify_predictions_partial_standard_case():
    """what if we do not necessarily want to change all the fields"""
    data = {
        "home_score": 40,
        "comment": "Another comment"
    }
    pred = Predictions.query.filter_by(id=3).first()
    assert pred.home_score != 40
    assert pred.comment is None
    mod = tipster.modify_prediction(data, pred)
    assert mod.home_score == 40
    assert mod.id == 3
    assert mod.comment == "Another comment"


def test_modify_predictions_border_case():
    """Fields that should not be changed"""
    data = {
        "fixture":"Manchester United - Harambee Stars"
    }
    pred = Predictions.query.filter_by(id=6).first()
    fix = pred.fixture
    assert pred.fixture != data['fixture']
    with pytest.raises(Exception):
        mod = tipster.modify_prediction(data, pred)
    assert pred.fixture == fix


def test_modify_predictions_wrong_border_case():
    """Now how about deformed or unknown field names"""
    data = {
        "coment": "Comment"
    }
    pred = Predictions.query.filter_by(id=6).first()
    with pytest.raises(Exception):
        mod = tipster.modify_prediction(data, pred)
    assert pred.comment is None

def test_delete_prediction():
    pred = Predictions.query.filter_by(id=5).first()
    assert pred is not None
    tipster.delete_prediction(pred_obj=pred)
    mod = Predictions.query.filter_by(id=5).first()
    assert mod is None