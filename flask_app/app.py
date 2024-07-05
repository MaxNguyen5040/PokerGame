from flask import Flask, render_template
import random

app = Flask(__name__)
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
pot = 0
global player_hands
bet_limit = 100

#_______________________App routes______________________
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/deal')
def deal():
    players_hands = deal_cards(2)  # deal to 2 players
    return {'players_hands': players_hands}

@app.route('/fold/<int:player_id>')
def fold(player_id):
    return f'Player {player_id} folds.'

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

current_player = 1
round_phase = 'deal'

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

@app.route('/ai_turn/<int:player_id>')
def ai_turn(player_id):
    ai_action_result = ai_action(player_id)
    return ai_action_result


#_________________Poker Game methods____________________
def create_deck():
    return [(rank, suit) for suit in suits for rank in ranks]

def deal_cards(num_players):
    deck = create_deck()
    random.shuffle(deck)
    return [deck[i::num_players] for i in range(num_players)]

def ai_action(player_id):
    # Add logic for AI player actions (fold, bet, etc.)
    return 'AI player folds.'

def determine_winner(player_hands):
    winner_id = 0
    winner_hand_rank = 'Straight'
    return jsonify({
        'player_id': winner_id + 1,
        'hand_rank': winner_hand_rank
    })


if __name__ == '__main__':
    app.run(debug=True)