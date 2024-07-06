import unittest
from app import app, save_game_state, load_game_state
from bots import PokerBot

class TestPokerGame(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_game_flow(self):
        response = self.app.post('/start_bot_actions')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Bots have made their moves', response.get_data(as_text=True))

    def test_save_load_game(self):
        save_game_state()
        load_game_state()
        # Check if game state is loaded correctly
        self.assertEqual(players[0].chips, 1000)  # Example assertion

if __name__ == '__main__':
    unittest.main()