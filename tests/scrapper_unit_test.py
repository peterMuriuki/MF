"""test secondary functions. the native functions  that enable the high level functions work"""
import unittest
from .golden_data import td, less_td, more_td
from bs4 import BeautifulSoup
from . import parse_table_rows as parse

class ScrapTests(unittest.TestCase):
    """refer to module documentation"""

    def setUp(self):
        self.td = [BeautifulSoup(td, 'html.parser')]
        self.less_td = [BeautifulSoup(less_td, 'html.parser')]
        self.more_td = [BeautifulSoup(more_td, 'html.parser')]

    def test_find_all(self):
        """finds the occurence of a string in disregard of presence of special characters in string"""
        pass
    
    def test_over_under(self):
        """cover all over/under market quotations variations"""

    def test_scrap(self):
        """the scrap function that translates several tds to a proper dictionary
        <tr>
            <td class="toolTyp" title=""><a href="typer,adrian1700,32702.html">adrian1700</a></td>
            <td>18:30</td>
            <td>Atalanta-Verona /Serie A</td>
            <td><a class="toolTypek" href="#forBET"
                   onclick="javascript:openUrl('https://www.iforbet.pl/rejestracja/yjlyfgkqbe ')">1 (-1)</a></td>
            <td>30.00</td>
            <td><a class="toolTypek" href="#forBET"
                   onclick="javascript:openUrl('https://www.iforbet.pl/rejestracja/yjlyfgkqbe ')">1.50</a></td>
            <td><a class="tableTypeBuk" style="color: " href="#Bet-At-Home"
                   onclick="javascript:openUrl('http://affiliates.bet-at-home.com/processing/clickthrgh.asp?btag=a_76140b_31922')"><img
                    class="bukImg" alt="Bet-At-Home" src="logo/7.jpg"/></a></td>
            <td><a rel="nofollow" href="art,7,Scores.html">Soccer</a></td>
            <td></td>
        </tr>
        """
        contained = ['tipster_name', 'tipster_url', 'fixture', 'time_of_play', 'sport', 'home_score', 'away_score',
                     'odds', 'pick', 'confidence', 'prediction_id']
        response = parse(self.td)
        self.assertTrue(type(response) is list)
        diction = response[0]
        self.assertTrue(type(diction) is dict)
        for key in contained:
            self.assertIn(key, diction.keys())
        self.assertTrue(diction['tipster_url'].startswith('http') and diction['tipster_url'].endswith('.html'))

    def test_scrap_border_cases(self):
        """calls the scrap on a deformed input specification: here we fail to include one or more tds
        pass in an empty td
        include extra tds in within the table row
        """
        response = parse(self.less_td)
        self.assertIs(type(response), list)
        self.assertFalse(response)

        self.less_td = None
        self.assertIs(type(response), list)
        self.assertFalse(response)

        response = parse(self.more_td)
        self.assertFalse(response)
        self.assertIs(type(response), list)

