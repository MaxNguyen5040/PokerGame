class Player:
    def __init__(self, player_id, name, chips=1000):
        self.id = player_id
        self.name = name
        self.chips = chips
        self.hand = []

    def adjust_chips(self, amount):
        self.chips += amount

    def receive_hand(self, hand):
        self.hand = hand

# Refactored game logic
def evaluate_winner(players, community_cards):
    hands = [player.hand + community_cards for player in players]
    scores = [evaluate_hand(hand) for hand in hands]
    return players[scores.index(max(scores))]

def play_round(players, community_cards):
    # Example round play logic
    for player in players:
        action = player.decide_action(game_state={})
        # Handle player actions
        if action == 'raise':
            amount = player.decide_amount()
            player.adjust_chips(-amount)
            pot_size += amount
        # Other actions: call, check, fold
    winner = evaluate_winner(players, community_cards)
    return winner