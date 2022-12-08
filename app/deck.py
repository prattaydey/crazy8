# Adorable Macho Elephants: Prattay, Joseph, Kevin, Anjini
# SoftDev
# Period 07
# Dec 2022

import requests

def create_deck():
    request = requests.get("https://deckofcardsapi.com/api/deck/new/")
    json = request.json()
    deck_id = json['deck_id']
    return deck_id

def shuffle_deck(deck_id):
    return requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/shuffle").json()

def draw_from_deck(deck_id):
    return requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw").json()['cards']

def draw_from_pile(deck_id, pile_name):
    return requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/{pile_name}/draw").json()['cards']

def setup(deck_id):
    shuffle_deck(deck_id)
    hand1 = ""
    hand2 = ""
    cards = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=16").json()['cards']
    for i in range(8):
        hand1 += cards[i]['code'] + ","
    for i in range(8, 16):
        hand2 += cards[i]['code'] + ","

    requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/player1/add/?cards={hand1}")
    requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/player2/add/?cards={hand2}")
    requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/play")

def get_pile_codes(deck_id, pile_name):
    pile = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/{pile_name}/list").json()['piles'][pile_name]['cards']
    pile_codes = []
    for card in pile:
        pile_codes.append(card['code'])
    return pile_codes

def get_pile_image_urls(deck_id, pile_name):
    pile = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/{pile_name}/list").json()['piles'][pile_name]['cards']
    pile_image_urls = []
    for card in pile:
        pile_image_urls.append(card['image'])
    return pile_image_urls



deck_id = create_deck()
setup(deck_id)
print("deck_id: " + deck_id)
print("url: " + f"https://deckofcardsapi.com/api/deck/{deck_id}")
print("player1: " + " ".join(get_pile_codes(deck_id, "player1")))
print("player2: " + " ".join(get_pile_codes(deck_id, "player2")))
print("player1: \n * " + "\n * ".join(get_pile_image_urls(deck_id, "player1")))