from flask import Flask, render_template, request, jsonify
import random
from bots import PokerBot, bots

app = Flask(__name__)
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
pot = 0
global player_hand1, player_hand2
bet_limit = 100
current_player = 1
round_phase = 'deal'

#_______________________App routes______________________
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deal')
def deal():
    players_hands = deal_cards(2)  # deal to 2 players
    return {'players_hands': players_hands}

def deal_cards(num_cards):
    deck = ['2H', '3H', '4H', '5H', '6H', '7H', '8H', '9H', 'TH', 'JH', 'QH', 'KH', 'AH',
            '2D', '3D', '4D', '5D', '6D', '7D', '8D', '9D', 'TD', 'JD', 'QD', 'KD', 'AD',
            '2C', '3C', '4C', '5C', '6C', '7C', '8C', '9C', 'TC', 'JC', 'QC', 'KC', 'AC',
            '2S', '3S', '4S', '5S', '6S', '7S', '8S', '9S', 'TS', 'JS', 'QS', 'KS', 'AS']
    return random.sample(deck, num_cards)

@app.route('/fold', methods=['POST'])
def fold():
    player_hand = []
    community_cards = []
    pot_size = 0
    message = 'You folded.'
    return jsonify({'message': message, 'player_hand': player_hand, 'community_cards': community_cards, 'pot_size': pot_size})


@app.route('/bet/<int:amount>')
def bet(amount):
    if amount > bet_limit:
        return f'Error: Bet exceeds limit of ${bet_limit}.'
    pot += amount
    return f'Bet ${amount} added to the pot. Total pot: ${pot}.'

@app.route('/get_pot')
def get_pot():
    global pot
    return f'Current pot size: ${pot}.'

@app.route('/start_round')
def start_round():
    return 'Round started. Cards dealt.'

@app.route('/flop')
def flop():
    return 'Flop round.'

@app.route('/turn')
def turn():
    return 'Turn round.'

@app.route('/river')
def river():
    return 'River round.'

@app.route('/next_turn')
def next_turn():
    global current_player, round_phase
    current_player = 2 if current_player == 1 else 1
    if round_phase == 'deal':
        round_phase = 'flop'
    elif round_phase == 'flop':
        round_phase = 'turn'
    elif round_phase == 'turn':
        round_phase = 'river'
    elif round_phase == 'river':
        round_phase = 'end'
    return f'Player {current_player}, it\'s your turn. Round phase: {round_phase}.'

@app.route('/player_action', methods=['POST'])
def player_action():
    action = request.form['action']
    global pot_size
    if action == 'check':
        message = 'You checked.'
    elif action == 'call':
        # Example: Match current bet amount, deduct from player's funds
        message = 'You called.'
    elif action == 'raise':
        amount = int(request.form['amount'])
        # Example: Increase the bet amount, deduct from player's funds
        pot_size += amount
        message = f'You raised by ${amount}.'
    return jsonify({'message': message, 'pot_size': pot_size})

@app.route('/start_round', methods=['POST'])
def start_new_round():
    game_state = start_round()
    return jsonify(game_state)

@app.route('/determine_winner', methods=['POST'])
def determine_winner():
    winner = evaluate_winner(player_hand, community_cards)
    message = f'{winner} wins the round!'
    return jsonify({'message': message, 'winner': winner})

@app.route('/end_round', methods=['POST'])
def end_round():
    global player_hand, community_cards, pot_size
    player_hand = []
    community_cards = []
    pot_size = 0
    return jsonify({'message': 'Round ended. Starting a new round...', 'player_hand': player_hand, 'community_cards': community_cards, 'pot_size': pot_size})

@app.route('/start_bot_actions', methods=['POST'])
def start_bot_actions():
    bot_actions()
    return jsonify({'message': 'Bots have made their moves.', 'pot_size': pot_size})

#_________________Poker Game methods____________________
def create_deck():
    return [(rank, suit) for suit in suits for rank in ranks]

def deal_cards(num_players):
    deck = create_deck()
    random.shuffle(deck)
    return [deck[i::num_players] for i in range(num_players)]

def evaluate_winner(player_hand, community_cards):
    combined_hand = player_hand + community_cards
    player_hand_type = classify_hand(combined_hand)
    return f'Player with {player_hand_type}'

def bot_actions():
    for bot in bots:
        action = bot.decide_action(game_state={})
        if action == 'raise':
            bot.adjust_chips(-10)  # Decrease chips for raising
            pot_size += 10  # Add to pot
        elif action == 'call':
            bot.adjust_chips(-5)  # Decrease chips for calling
            pot_size += 5  # Add to pot
        # Other actions: check, fold

def start_round():
    player_hand = deal_cards(2)  # Function to deal cards
    community_cards = deal_cards(5)  # Function to deal community cards
    pot_size = 0  # Reset pot size
    return {'player_hand': player_hand, 'community_cards': community_cards, 'pot_size': pot_size}

def classify_hand(hand):
    # Simplified example logic to classify hand
    ranks = '23456789TJQKA'
    suits = 'HDCS'
    rank_count = {rank: sum(card[0] == rank for card in hand) for rank in ranks}
    suit_count = {suit: sum(card[1] == suit for card in hand) for suit in suits}

    if 5 in suit_count.values():
        return 'Flush'
    if 4 in rank_count.values():
        return 'Four of a Kind'
    if 3 in rank_count.values() and 2 in rank_count.values():
        return 'Full House'
    if 3 in rank_count.values():
        return 'Three of a Kind'
    if list(rank_count.values()).count(2) == 2:
        return 'Two Pair'
    if 2 in rank_count.values():
        return 'Pair'
    return 'High Card'

if __name__ == '__main__':
    app.run(debug=True)