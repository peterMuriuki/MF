"""Defines some of the data members that will form as the basis of comparison in our tests
this was done so as to reduce the verbosity of the test functions and help keep them simple
"""

td = """<tr><td class="toolTyp" title=""><a href="typer,adrian1700,32702.html">adrian1700</a></td><td>18:30</td><td>Atalanta-Verona /Serie A</td><td><a class="toolTypek" href="#forBET" onclick="javascript:openUrl('https://www.iforbet.pl/rejestracja/yjlyfgkqbe ')">1 (-1)</a></td><td>30.00</td><td><a class="toolTypek" href="#forBET" onclick="javascript:openUrl('https://www.iforbet.pl/rejestracja/yjlyfgkqbe ')">1.50</a></td><td>  <a class="tableTypeBuk" style="color: " href="#Bet-At-Home" onclick="javascript:openUrl('http://affiliates.bet-at-home.com/processing/clickthrgh.asp?btag=a_76140b_31922')"><img class="bukImg" alt="Bet-At-Home" src="logo/7.jpg" /></a></td><td><a rel="nofollow" href="art,7,Scores.html">Soccer</a></td><td></td></tr>"""
less_td = """<tr><td class="toolTyp" title=""><a href="typer,adrian1700,32702.html">adrian1700</a></td><td>18:30</td><td><a class="toolTypek" href="#forBET" onclick="javascript:openUrl('https://www.iforbet.pl/rejestracja/yjlyfgkqbe ')">1 (-1)</a></td><td>30.00</td><td><a class="toolTypek" href="#forBET" onclick="javascript:openUrl('https://www.iforbet.pl/rejestracja/yjlyfgkqbe ')">1.50</a></td><td>  <a class="tableTypeBuk" style="color: " href="#Bet-At-Home" onclick="javascript:openUrl('http://affiliates.bet-at-home.com/processing/clickthrgh.asp?btag=a_76140b_31922')"><img class="bukImg" alt="Bet-At-Home" src="logo/7.jpg" /></a></td><td></td></tr>"""
more_td = """<tr><td class="toolTyp" title=""><a href="typer,adrian1700,32702.html">adrian1700</a></td><td>18:30</td><td>Atalanta-Verona /Serie A</td><td><a class="toolTypek" href="#forBET" onclick="javascript:openUrl('https://www.iforbet.pl/rejestracja/yjlyfgkqbe ')">1 (-1)</a></td><td>30.00</td><td><a class="toolTypek" href="#forBET" onclick="javascript:openUrl('https://www.iforbet.pl/rejestracja/yjlyfgkqbe ')">1.50</a></td><td>  <a class="tableTypeBuk" style="color: " href="#Bet-At-Home" onclick="javascript:openUrl('http://affiliates.bet-at-home.com/processing/clickthrgh.asp?btag=a_76140b_31922')"><img class="bukImg" alt="Bet-At-Home" src="logo/7.jpg" /></a></td><td><a rel="nofollow" href="art,7,Scores.html">Soccer</a></td><td></td><td><a rel="nofollow" href="art,7,Scores.html">Soccer</a></td><td></td></tr>"""

from bs4 import BeautifulSoup

def soupify(element):
    return BeautifulSoup(element, 'html.parser')

