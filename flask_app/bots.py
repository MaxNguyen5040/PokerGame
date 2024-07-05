class PokerBot:
    def __init__(self, bot_id, name):
        self.bot_id = bot_id
        self.name = name
        self.hand = []
        self.chips = 1000  # Initial chip count

    def decide_action(self, game_state):
        # Basic decision-making logic (random for now)
        import random
        actions = ['check', 'call', 'raise', 'fold']
        return random.choice(actions)

    def receive_hand(self, hand):
        self.hand = hand

    def adjust_chips(self, amount):
        self.chips += amount

# Initialize bots
bots = [PokerBot(bot_id=i, name=f'Bot {i}') for i in range(1, 5)]
