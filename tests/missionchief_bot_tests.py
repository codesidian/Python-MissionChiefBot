import unittest
import sys
import src.missionchief_bot as Bot

class TestMissionChiefBot(unittest.TestCase):

    def testLogin(self):
        username="Fake"
        password="News"
        self.assertFalse(Bot.login(username,password))
        username="pybottest@live.com"
        password="123456"
        self.assertTrue(Bot.login(username,password))

    def testMissions(self):
        self.assertTrue(Bot.getMissions())

if __name__ == '__main__':
    unittest.main()