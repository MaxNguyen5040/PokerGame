from collections import Counter

def evaluate_hand_strength(hand):
    values = sorted(['--23456789TJQKA'.index(card[0]) for card in hand])
    suits = [card[1] for card in hand]
    value_counts = Counter(values)
    suit_counts = Counter(suits)

    if len(suit_counts) == 1 and values == list(range(values[0], values[0] + 5)):
        return "Straight Flush", 8
    elif 4 in value_counts.values():
        return "Four of a Kind", 7
    elif sorted(value_counts.values()) == [2, 3]:
        return "Full House", 6
    elif len(suit_counts) == 1:
        return "Flush", 5
    elif values == list(range(values[0], values[0] + 5)):
        return "Straight", 4
    elif 3 in value_counts.values():
        return "Three of a Kind", 3
    elif list(value_counts.values()).count(2) == 2:
        return "Two Pair", 2
    elif 2 in value_counts.values():
        return "One Pair", 1
    else:
        return "High Card", 0

def hand_rank(hand):
    hand_type, rank = evaluate_hand_strength(hand)
    sorted_values = sorted(['--23456789TJQKA'.index(card[0]) for card in hand], reverse=True)
    return rank, sorted_values