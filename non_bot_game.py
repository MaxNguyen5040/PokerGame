import random
from collections import Counter
from hand_evaluator import hand_rank, evaluate_hand_strength

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank}{self.suit}"
    
class Deck:
    suits = ['H', 'D', 'C', 'S']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']

    def __init__(self):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)

    def deal(self, num_cards):
        return [self.cards.pop() for _ in range(num_cards)]

class Player:
    def __init__(self, name, chips=1000):
        self.name = name
        self.chips = chips
        self.hand = []

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def bet(self, amount):
        if amount > self.chips:
            raise ValueError(f"{self.name} doesn't have enough chips to bet {amount}.")
        self.chips -= amount
        return amount

class PokerGame:
    def __init__(self, players):
        self.players = players
        self.deck = Deck()
        self.pot = 0
        self.community_cards = []

    def deal_hands(self):
        for player in self.players:
            player.receive_cards(self.deck.deal(2))

    def deal_community_cards(self, num_cards):
        self.community_cards.extend(self.deck.deal(num_cards))

    def betting_round(self):
        for player in self.players:
            try:
                bet_amount = player.bet(random.randint(1, player.chips))
                self.pot += bet_amount
            except ValueError as e:
                print(e)

    def play_hand(self):
        self.deal_hands()
        self.betting_round()
        self.deal_community_cards(3)  # Flop
        self.betting_round()
        self.deal_community_cards(1)  # Turn
        self.betting_round()
        self.deal_community_cards(1)  # River
        self.betting_round()
        hand_result = self.evaluate_winner()
        print(hand_result)

    def evaluate_winner(self):
        player_hands = {player.name: player.hand + self.community_cards for player in self.players}
        best_hand = None
        best_rank = (-1, [])

        for player, hand in player_hands.items():
            rank = hand_rank(hand)
            if rank > best_rank:
                best_hand = (player, hand)
                best_rank = rank

        winner, winning_hand = best_hand
        winning_hand_type, _ = evaluate_hand_strength(winning_hand)

        return {
            'winner': winner,
            'winning_hand': winning_hand_type,
            'pot': self.pot,
            'player_hands': player_hands
        }

if __name__ == "__main__":
    players = [Player("Player1"), Player("Player2")]
    game = PokerGame(players)
    game.play_hand()