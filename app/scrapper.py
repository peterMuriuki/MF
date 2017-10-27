"""
 Home Page: typersi.com Areas of interests
    picks from tipsters with the best efficiency -> high precedence
    most repeated predictions from the general full all predictions page

    This module is the toolbox of all scrapping and organisation of return data which
    will be mostly inform of basic python objects -> mostly dictionary
 """
import re, sys, requests
from datetime import datetime
from bs4 import BeautifulSoup
from .models import Predictions, Tipster

tipster = Tipster()


def get_home_page(text=False):
    """returns either a soup object or string object as per the given arguments
     soup_object by default"""
    home_url = 'http://www.typersi.com'
    index_html = requests.get(home_url).text
    if text:
        # return a text reponse
        return index_html
    soup = BeautifulSoup(index_html, 'html.parser')
    return soup


def get_efficient_table(soup):
    """return the table that contains tips from the most efficient tipsters"""
    h2_string = "Picks from tipsters with the best efficiency"
    if len(re.findall(h2_string, str(soup))):
        best_5_header = soup.find_all('h2', string=h2_string)[0]
    else:
        print("Extreme danger!.. site's relative structure compromised, re-evaluate")
        sys.exit(2)
    desired_table = best_5_header.next_sibling.next_sibling
    return desired_table


def get_picks_from_tipsters_with_the_best_efficiency(soup):
    """"""
    desired_table = get_efficient_table(soup)
    # i have just thought of a way to check if the desired table is indeed what we are looking
    # for, well at least to some point, like say what if we had a way of accessing its attributes
    # and asserting what we know should be present is in-fact present
    tbody = desired_table.tbody
    tr_list = tbody.find_all('tr')
    data_list = parse_table_rows(tr_list)
    _response = {"efficient": data_list}
    return _response


def get_all_tips_desired_table(soup):
    """ Parses the pozostali remainder page and extracts the table with all the tips"""
    h2_string = "other picks list:"
    if len(re.findall(h2_string, str(soup))):
        best_5_header = soup.find_all('h2', string=h2_string)[0]
    else:
        print("Extreme danger!.. site's relative structure compromised, re-evaluate")
        sys.exit(2)
    desired_table = best_5_header.next_sibling.next_sibling
    return desired_table


def get_all_other_tips():
    """ input: soup object representing the full webpage
    process: retrieve the others link and extract all the other remaining tips
    flagging procedure will be based on the tip that appears more than once."""
    pozostali_url = '''http://www.typersi.com/pozostali,remainder.html'''
    page_html = requests.get(pozostali_url)
    soup = BeautifulSoup(page_html)
    # eff_table = get_efficient_table(soup)
    # desired_table = eff_table.next_sibling.next_sibling.next_sibling.next_sibling - > for the usual unlabeled home page table
    # we need to redefine how to get the desired table
    desired_table = get_all_tips_desired_table(soup)
    tbody = desired_table.tbody
    tr_list = tbody.find_all('tr')
    data_list = parse_table_rows(tr_list)
    _response = {"all": data_list}
    return _response


def all_tips_occurrence_checker(diction):
    """input: dictionary with the key 'all' that contains a list that has the scrapped and formatted data
    output: a dictionary with a key value that denotes the value """
    check_string = ''
    # diction = json_response
    data_list = diction['all']
    for diction in data_list:
        temp_string = diction['home_team'][:2] + diction['away_team'][:2] + diction['pick']
        check_string += temp_string
        count = len(re.findall(temp_string, check_string))
        diction['count'] = count
    return diction


def all_other_tips_compiler(soup):
    """will be in-charge of looking at the dictionaries that have the count key and retrieve those with a count greater
    than one"""
    dict_response = get_all_other_tips(soup)
    doi = all_tips_occurrence_checker(dict_response)  # doi dictionary of interest
    data_list = doi['all']
    for diction in data_list:
        if diction['count'] > 1:
            tipster.add_prediction(diction)
    return True


def parse_table_rows(tr_list):
    """ extracts the data from the html table rows"""
    return_list = list()
    for tr in tr_list:
        temp_diction = {}
        td_list = tr.find_all('td')
        # validating the number of tds in that we have just captured
        if len(td_list) != 9:
            raise Exception('Problem getting the table data')
        # tipster details in the first td
        first_td = td_list[0]
        tipster_url = 'http://www.typersi.com/' + first_td.a.get('href')
        tipster_name = first_td.a.get_text()
        # timing functionality
        second_td =td_list[1]
        time_as_string = second_td.get_text()
        if len(re.findall(':', time_as_string)):
            time_as_list = time_as_string.split(':')
        else:
            time_as_list = time_as_string.split(',')
        hour = int(time_as_list[0])
        minute = int(time_as_list[1])
        today = datetime.today()
        time_of_play = datetime(today.year, today.month, today.day, hour, minute)
        # the match including both the home team and the away team
        third_td = td_list[2]
        match = third_td.get_text()
        if match.find('-'):
            home_and_away = match.split(' - ')
        elif match.find('vs'):
            home_and_away = match.split(' vs ')
        home_team = home_and_away[0]
        away_team = home_and_away[1]
        # the pick
        fourth_td = td_list[3]
        if len(re.findall(r'\d', fourth_td.get_text())) > 0:
            pick = str(fourth_td.get_text())
        else:
            pick = str(fourth_td.get_text().strip(' '))
        # the proposed stake
        fifth_td = td_list[4]
        proposed_stake = fifth_td.get_text()
        stake_as_float = float(proposed_stake)
        confidence = stake_as_float / 30.0 * 100
        confidence = confidence
        # now to a very important part to the odds
        sixth_td = td_list[5]
        odds_as_string = sixth_td.get_text()
        odds = float(odds_as_string)
        # as for the results i.e if provided
        results_td = td_list[-2]
        results = results_td.get_text()
        if len(re.findall('\d', results)) == 0:
            # signifies that the there is no digit in the result and thus the score is not yet displayed
            result = None
        temp_diction['tipster_url'] = tipster_url
        temp_diction['tipster_name'] = tipster_name
        temp_diction['time_of_play'] = time_of_play.__str__()
        temp_diction['home_team'] = home_team
        temp_diction['away_team'] = away_team
        temp_diction['pick'] = pick
        temp_diction['confidence'] = confidence
        temp_diction['odds'] = odds
        temp_diction = prediction_id_generator(temp_diction)
        if instance_unique_checker(temp_diction['prediction_id']):
            tipster.add_prediction(temp_diction)
        return_list.append(temp_diction)
    return return_list


def prediction_id_generator(diction):
    """input: dict object.
    will add a new key, value combination to the diction derived from  the important values.
    of the argument diction
    output: the updated diction"""
    # important parts: h_t, a_t, tipster_name, predition.
    pred_id = diction['tipster_name'] + diction['home_team'][:3] + diction['away_team'][:3] + diction['pick']
    diction['prediction_id'] = pred_id
    return diction


def instance_unique_checker(pred_id):
    """i need  function that will be able to check that a certain prediction is different from
    from another that is already in the current single instance of the system.
     my first idea is to generate some sort of id
    that is inclusive of the primary parts of the prediction."""
    # output: true if diction record is new or False if record is already existent
    response = Predictions.query.filter_by(prediction_id=pred_id).first()
    if response:
        return False
    elif response is None:
        return True

def get_optimum_three(soup):
    """I think there is a side of this that i think we are not considering,.. instead of randomly picking
    matches whose odds are going to line up with our target how about picking these matches from a more specialised
    pool. A pool that we have also filtered through"""
    # input is from the tipsters with the best efficiency
    pass

def run():
    """run the get efficient tips commands"""
    soup = get_home_page()
    get_picks_from_tipsters_with_the_best_efficiency(soup)

if __name__ == '__main__':
    run()
