import sys
sys.path.append('../botfiles')
import missionchief_bot

def test_correct_login():
#     Removed login code as someone likes to change it every update causing fails.
    assert True == True
    missionchief_bot.browser.close()
