import sys
sys.path.append('../botfiles')
import missionchief_bot

def test_correct_login():
    assert missionchief_bot.login('1232131132321322132','1232131132321322132',missionchief_bot.browser) == True
    missionchief_bot.browser.close()
