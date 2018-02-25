"""
 Home Page: typersi.com Areas of interests
    picks from tipsters with the best efficiency -> high precedence
    most repeated predictions from the general full all predictions page
    This module is the toolbox of all scrapping and organisation of return data which
    will be mostly inform of basic python objects -> mostly dictionary
 """
import re, requests
from datetime import datetime
from bs4 import BeautifulSoup
from .models import Predictions, Tipster
from .omy import ElementError
# from .email import ToAdmin
import schedule

tipster = Tipster()


def get_home_page(text=False, file=None):
    """
    returns either a soup object or string object as per the given arguments
     soup_object by default
     """
    if file is None:
        home_url = 'http://www.typersi.com'
        index_html = requests.get(home_url).text
    else:
        # read files and return text
        file_handler = open(file, 'r')
        contents = file_handler.read()
        index_html = contents
    if text:
        # return a text response
        return index_html
    soup = BeautifulSoup(index_html, 'html.parser')
    return soup


def get_efficient_table(soup):
    """return the table that contains tips from the most efficient tipsters"""
    h2_string = "Picks from tipsters with the best efficiency"
    if len(re.findall(h2_string, str(soup))):
        best_5_header = soup.find_all('h2', string=h2_string)[0]
    else:
        raise ElementError("Extreme danger!.. site's relative structure compromised, re-evaluate")
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
    # add count
    for diction in data_list:
        diction['count'] = 0
    _response = {"efficient": data_list}
    save_prediction(data_list)
    return _response


def get_all_tips_desired_table(soup):
    """ Parses the pozostali remainder page and extracts the table with all the tips"""
    h2_string = "other picks list:"
    if len(re.findall(h2_string, str(soup))):
        best_5_header = soup.find_all('h2', string=h2_string)[0]
    else:
        raise ElementError("Extreme danger!.. site's relative structure compromised, re-evaluate")
    desired_table = best_5_header.next_sibling.next_sibling
    return desired_table


def get_all_other_tips(file=None):
    """ input: soup object representing the full webpage
    process: retrieve the others link and extract all the other remaining tips
    flagging procedure will be based on the tip that appears more than once."""
    if file is None:
        pozostali_url = '''http://www.typersi.com/pozostali,remainder.html'''
        page_html = requests.get(pozostali_url)
        page_text = page_html.text
    else:
        with open(file, 'r') as file_handler:
            page_text = file_handler.read()

    soup = BeautifulSoup(page_text, 'html.parser')
    desired_table = get_all_tips_desired_table(soup)
    tbody = desired_table.tbody
    tr_list = tbody.find_all('tr')
    data_list = parse_table_rows(tr_list)
    all_other_tips_compiler(data_list) 
    return {"all":data_list}


def over_under(string):
    """Take in a string and determine if the string denotes a pick whose market is the over/under"""
    string = str.upper(string)
    if string.find('OVER') > 0:
        return True
    elif string.find('+') > 0:
        return True
    elif string.find('OV') > 0:
        return True
    return False


def find_all(pattern, string):
    """"""
    count, start, index = 0, 0, 0
    while index <= len(string):
        index = string.find(pattern, start, len(string))
        if index < 0:
            return count
        else:
            count += 1
            start  = index + len(pattern)
    return count


def all_tips_occurrence_checker(data_list):
    """input:  list that has the scrapped and formatted data
    output: a list of dictionaries with a key count value that denotes the value """
    # i think several picks can be saying the same thing in a different way and they should
    # compiled so that the physical representation does not harbour this process
    check_string = ''
    for diction in data_list:
        temp_string = diction['fixture'] + diction['pick']
        check_string += temp_string
    for diction in data_list:
        temp_string = diction['fixture'] + diction['pick']
        count = find_all(temp_string, check_string)
        diction['count'] = count
        if over_under(diction['pick']):
            diction['count'] = len(data_list)
    return data_list


def all_other_tips_compiler(data_list):
    """
    Input : data_list: a list of dictionaries
    will be in-charge of looking at the dictionaries that have the count key and retrieve those with a count greater
    than one"""
    doi = all_tips_occurrence_checker(data_list)  # list of interest
    email_message = []
    for diction in doi:
        if diction['count'] > 1 and instance_unique_checker(diction['prediction_id']) and prediction_uniqueness_checker(diction):
            tipster.add_prediction(diction)
            email_message.append(diction)
    # need to send email here
    # ToAdmin.new_prediction(email_message)
    return True


def parse_table_rows(tr_list):
    """ extracts the data from the html table rows"""
    return_list = list()

    def get_tipster(td_list):
        """
        :param td_list:
        :return:
        tipster details in the first td
        """
        first_td = td_list[0]
        tipster_url = 'http://www.typersi.com/' + first_td.a.get('href').strip()
        tipster_name = first_td.a.get_text().strip()
        return tipster_url, tipster_name

    def get_time(td_list):
        """retrieves the time of play... warn against undefined utc zones"""
        # timing functionality
        second_td = td_list[1]
        time_as_string = second_td.get_text()
        hour = time_splitter(time_as_string)[0]
        minute = time_splitter(time_as_string)[1]
        today = datetime.today()
        time_of_play = datetime(today.year, today.month, today.day, hour, minute)
        time_of_play.hour + 1
        return time_of_play

    def get_fixture(td_list):
        """get the match info: includes both the home and away teams"""
        # the fixture including both the home team and the away team
        third_td = td_list[2]
        fixture = third_td.get_text().strip()
        return fixture

    def get_pick(td_list):
        """retrieve the pick"""
        # the pick
        fourth_td = td_list[3]
        if len(re.findall(r'\d', fourth_td.get_text())) > 0:
            pick = str(fourth_td.get_text()).strip()
        else:
            pick = str(fourth_td.get_text().strip(' '))
        return pick

    def get_confidence(td_list):
        """scraps off the confidence level of a tip"""
        fifth_td = td_list[4]
        proposed_stake = fifth_td.get_text()
        stake_as_float = float(proposed_stake)
        confidence = stake_as_float / 30.0 * 100
        confidence = round(confidence)
        return confidence

    def get_odds(td_list):
        """"""
        # now to a very important part to the odds
        sixth_td = td_list[5]
        odds_as_string = sixth_td.get_text()
        odds = float(odds_as_string)
        return odds

    def get_sport(td_list):
        """Retrieves either the sport or the result since the appearance of the two is mutually inclusive->
        However it is my intention that they are both saved separately"""
        # as for the results i.e if provided
        results_td = td_list[-2]
        results = results_td.get_text()
        if len(re.findall('\d', results)) == 0:
            # signifies that the there is no digit in the result and thus the score is not yet displayed
            home_score = None
            away_score = None
            sport = results
        else:
            home_score = re.findall('\d', results)[0]
            away_score = re.findall('\d', results)[1]
            sport = None

        return home_score, away_score, sport


    for tr in tr_list:
        try:
            temp_diction = {}
            td_list = tr.find_all('td')
            # validating the number of tds in that we have just captured
            if len(td_list) > 9 or len(td_list) < 8:
                raise ElementError('Problem getting the table data')
            temp_diction['tipster_url'], temp_diction['tipster_name'] = get_tipster(td_list)
            temp_diction['time_of_play'] = get_time(td_list)
            temp_diction['fixture'] = get_fixture(td_list)
            temp_diction['pick'] = get_pick(td_list)
            temp_diction['confidence'] = get_confidence(td_list)
            temp_diction['odds'] = get_odds(td_list)
            temp_diction['home_score'], temp_diction['away_score'], temp_diction['sport'] = get_sport(td_list)
            temp_diction = prediction_id_generator(temp_diction)
            return_list.append(temp_diction)
        except ElementError:
            continue
    return return_list

  
def save_prediction(data):
    """The workaround, the functions incharge of requesting the respecive data will also be incharge of saving the predictions"""
    # this function should work for many dictionaries or even one dictioary instance
    email_message = []
    for diction in data:
        if instance_unique_checker(diction['prediction_id']) and prediction_uniqueness_checker(diction):
            tipster.add_prediction(diction)
            email_message.append(diction)
    # need to send email here
    # ToAdmin.new_prediction(email_message)
    return True


def prediction_id_generator(diction):
    """input: dict object.
    will add a new key, value combination to the diction derived from  the important values.
    of the argument diction
    output: the updated diction"""
    # important parts: h_t, a_t, tipster_name, predition.
    pred_id = diction['tipster_name'] + diction['fixture'][2:7] + diction['pick']
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


def prediction_uniqueness_checker(diction):
    """
    :param: a dictionary instance of the prediction data to be checked if existent
    checks if the prediction's pick is existent and returns False if found else returns True """
    response = Predictions.query.filter_by(fixture=diction['fixture']).filter_by(pick=diction['pick']).first()
    if response:
        return False
    elif response is None:
        return True


def time_splitter(string):
    """This function will derive the hour and minutes that a game will be played from a string
    it will also check the integrity of such a time"""
    # date format is -> two digits, a separator and another two digits
    pattern = r'\d+'
    time_list = re.findall(pattern, string)
    hour, minute = 0, 0
    if len(time_list) != 2:
        # send an email to admin
        pass
    try:
        hour = int(time_list[0])
        minute = int(time_list[1])
    except :
        #send an email: refused to cast into integer
        pass
    if not 0 <= hour < 24 and not 0 <= minute < 60:
        # send an email: data integrity broken
        pass
    return [hour, minute]


def run():
    """run the get efficient tips commands"""
    try:
        soup = get_home_page()
        get_picks_from_tipsters_with_the_best_efficiency(soup)
    except ElementError as e:
        # send email for confirmation to admin and log issue
        # ToAdmin.error(e.__repr__())
        pass
    try:
        get_all_other_tips()
    except ElementError as e:
        # send email for confirmation to admin and log issue
        # ToAdmin.error(e.__repr__())
        pass

def initiate():
    """:param: None
    :-> Use schedule to well,.. schedule"""
    run()
    schedule.every(2).hours.do(run)

    while True:
        schedule.run_pending()


if __name__ == '__main__':
    run()
