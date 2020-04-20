import sys
sys.path.append('../botfiles')
import missionchief_bot

def test_correct_login():
    assert missionchief_bot.login('ambostest1233','ambostest1233',missionchief_bot.browser) == True
    missionchief_bot.browser.close()
