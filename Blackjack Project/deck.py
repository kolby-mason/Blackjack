import random

suit = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
deck = [(card, category) for category in suit for card in cards_list]

def shuffle_deck():
    random.shuffle(deck)

def deal_card():
    return deck.pop()

def reset_deck():
    global deck
    deck = [(card, category) for category in suit for card in cards_list]
