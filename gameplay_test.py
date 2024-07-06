from bots import PokerBot, bot_actions, evaluate_hand
import random

def simulate_game():
    bots = [PokerBot(bot_id=i, name=f'Bot_{i}') for i in range(4)]
    for bot in bots:
        bot.receive_hand(['2H', '3D', '5S', '9C', 'KD'])  # Example hand
    
    for _ in range(100):  # 100 rounds
        bot_actions()
        outcome = 'win' if random.random() > 0.5 else 'lose'
        for bot in bots:
            bot.learn(outcome)
            bot.adjust_chips(100 if outcome == 'win' else -100)

    for bot in bots:
        print(f'{bot.name} strategy: {bot.strategy}')

def deal_hand():
    suits = ['H', 'D', 'S', 'C']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    deck = [rank + suit for rank in ranks for suit in suits]
    random.shuffle(deck)
    return deck[:5]

if __name__ == '__main__':
    simulate_game()
