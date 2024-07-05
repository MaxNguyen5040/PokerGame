from flask import Flask, render_template
import random

app = Flask(__name__)
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
pot = 0

#App routes
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
    global pot
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

#Poker Game methods

def create_deck():
    return [(rank, suit) for suit in suits for rank in ranks]

def deal_cards(num_players):
    deck = create_deck()
    random.shuffle(deck)
    return [deck[i::num_players] for i in range(num_players)]



if __name__ == '__main__':
    app.run(debug=True)