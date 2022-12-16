# Adorable Macho Elephants: Prattay, Joseph, Kevin, Anjini
# SoftDev
# Period 07
# Dec 2022

import requests
import json

blobId = 1051631725620510720

def create_deck():
    request = requests.get("https://deckofcardsapi.com/api/deck/new/")
    json = request.json()
    deck_id = json['deck_id']
    return deck_id

def shuffle_deck(deck_id):
    return requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/shuffle").json()

def draw_from_deck(deck_id):
    return requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw").json()['cards'][0]

def draw_from_pile(deck_id, pile_name):
    return requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/{pile_name}/draw").json()['cards'][0]

#creates 2 hands, each one with 8 cards 
def setup(deck_id):
    shuffle_deck(deck_id)
    hand1 = ""
    hand2 = ""
    cards = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=16").json()['cards']
    for i in range(8):
        hand1 += cards[i]['code'] + ","
    for i in range(8, 16):
        hand2 += cards[i]['code'] + ","
    starting_card = draw_from_deck(deck_id)['code']

    requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/player1/add/?cards={hand1}")
    requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/player2/add/?cards={hand2}")
    requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/play/add/?cards={starting_card}")

def get_pile(deck_id, pile_name):
    pile = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/{pile_name}/list").json()['piles'][pile_name]['cards']
    return pile

def upload_deck_id(deck_id, room_name):
    # get a dictionary of existing rooms and their ids
    url = f"https://jsonblob.com/api/room/{blobId}"
    existing_ids = requests.get(url).content
    existing_ids = json.loads(existing_ids)
    existing_ids = dict(existing_ids)
    #print(existing_ids['test'])

    existing_ids.update({deck_id : {"room_name" : room_name}})
    data = json.dumps(existing_ids)
    
    requests.put(url, data=data)
    return url

def get_rooms():
    url = f"https://jsonblob.com/api/room/{blobId}"
    request = requests.get(url)
    rooms = json.loads(request.content)
    return dict(rooms)

# helper function -- draws card from the hand that has it, adds to pile in play
def play_card(deck_id, card_code):
    return requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/play/add/?cards={card_code}")

# checks to see if card is valid to deal
def card_check(deck_id, player_card):
    top_card = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/play/").json()['cards'][0]
    if player_card['suit'] == top_card['suit'] or player_card['value'] == top_card['value']:
        card_code = player_card['code']
        return play_card(deck_id, card_code)
    return False

# adds a card to a pile 
def add_to_pile(pile_name, ):
    pile_name["play"] = "red"
    return 1

# does what it says 
def add_player(deck_id, username):
    # get a dictionary of all the rooms
    rooms = get_rooms()
    # tell the dictionary that it's a dictionary
    room_dict = dict(rooms[deck_id])

    if not 'player1' in room_dict:
        room_dict.update({"player1" : username})
    elif not 'player2' in room_dict:
        room_dict.update({"player2" : username})
    else:
        return False

    # replace the current definition for deck_id with the modified one
    rooms[deck_id] = room_dict

    # upload the data
    rooms = json.dumps(rooms)
    print(rooms)
    url = f"https://jsonblob.com/api/room/{blobId}"
    requests.put(url, data=rooms)

    return True

def remove_player(deck_id, username):
    # get a dictionary of all the rooms
    rooms = get_rooms()
    # tell the dictionary it's a dictionary
    room_dict = dict(rooms[deck_id])

    # if the user isn't in 
    # player_names = room_dict.values()
    # if username not in player_names:
    #     return False

    if 'player1' in room_dict and room_dict['player1'] == username:
        room_dict.pop('player1')
    elif 'player2' in room_dict and room_dict['player2'] == username:
        room_dict.pop('player2')

    rooms[deck_id] = room_dict

    # upload
    rooms = json.dumps(rooms)
    url = f"https://jsonblob.com/api/room/{blobId}"
    requests.put(url, data=rooms)

    return True

def remaining_in_deck(deck_id):
    get_deck = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}").json()


print("https://jsonblob.com/api/room/1051631725620510720")
# deck_id = create_deck()
# setup(deck_id)
# print("deck_id: " + deck_id)
# print("url: " + f"https://deckofcardsapi.com/api/deck/{deck_id}")
# print("player1: " + " ".join(get_pile_codes(deck_id, "player1")))
# print("player2: " + " ".join(get_pile_codes(deck_id, "player2")))
# print("player1: \n * " + "\n * ".join(get_pile_image_urls(deck_id, "player1")))
# print(upload_deck_id(deck_id, "test2"))
# print(get_rooms())
