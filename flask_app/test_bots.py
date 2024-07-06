import unittest
from bots import PokerBot

class TestPokerBot(unittest.TestCase):
    def setUp(self):
        self.bot = PokerBot(bot_id=1, name='TestBot')

    def test_decide_action(self):
        decision = self.bot.decide_action(game_state={'pot_size': 100})
        self.assertIn(decision['action'], ['check', 'call', 'raise', 'fold'])

    def test_adjust_chips(self):
        self.bot.adjust_chips(-100)
        self.assertEqual(self.bot.chips, 900)

    def test_learn(self):
        self.bot.history = [('0.5-100', 'call'), ('0.7-200', 'raise')]
        self.bot.learn(outcome='win')
        self.assertGreater(self.bot.strategy['0.5-100'], 0)
        self.assertGreater(self.bot.strategy['0.7-200'], 0)

    def test_strategy_update(self):
        self.bot.strategy['0.5-100'] = 0.2
        self.bot.history = [('0.5-100', 'call')]
        self.bot.learn(outcome='win')
        self.assertGreater(self.bot.strategy['0.5-100'], 0.2)

if __name__ == '__main__':
    unittest.main()
