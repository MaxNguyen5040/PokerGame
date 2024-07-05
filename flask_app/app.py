from flask import Flask, render_template
import random

app = Flask(__name__)
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']

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

@app.route('/bet/<int:player_id>/<int:amount>')
def bet(player_id, amount):
    return f'Player {player_id} bets ${amount}.'

def create_deck():
    return [(rank, suit) for suit in suits for rank in ranks]

def deal_cards(num_players):
    deck = create_deck()
    random.shuffle(deck)
    return [deck[i::num_players] for i in range(num_players)]



if __name__ == '__main__':
    app.run(debug=True)