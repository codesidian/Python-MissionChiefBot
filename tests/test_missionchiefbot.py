import sys
sys.path.append('../botfiles')
import missionchief_bot

def test_correct_login():
    assert missionchief_bot.login('hellouk133334','lol123',missionchief_bot.browser) == True
    missionchief_bot.browser.close()
