import unittest
from bots import PokerBot

class TestPokerBot(unittest.TestCase):
    def setUp(self):
        self.bot = PokerBot(bot_id=1, name='TestBot')

    def test_decide_action(self):
        decision = self.bot.decide_action(game_state={})
        self.assertIn(decision['action'], ['check', 'call', 'raise', 'fold'])

    def test_adjust_chips(self):
        self.bot.adjust_chips(-100)
        self.assertEqual(self.bot.chips, 900)

if __name__ == '__main__':
    unittest.main()