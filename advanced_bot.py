class AdvancedBot(Player):
    def __init__(self, name, stack):
        super().__init__(name, stack)

    def make_decision(self, game_state):
        opponent_hand_strength = self.estimate_opponent_hand_strength(game_state)
        hand_strength = self.evaluate_hand_strength(game_state)
        
        if hand_strength > opponent_hand_strength:
            return self.bet(game_state)
        elif random.random() < 0.2:
            return self.bluff(game_state)
        else:
            return self.fold()

    def evaluate_hand_strength(self, game_state):
        # Simplified hand strength evaluation
        return random.random()

    def bet(self, game_state):
        return 'bet', min(game_state['pot'] // 2, self.stack)

    def bluff(self, game_state):
        return 'bet', min(game_state['pot'], self.stack)

    def fold(self):
        return 'fold', 0