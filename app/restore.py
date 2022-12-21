import requests
import json
from deck import *
import deck
blobId = 1051631725620510720

def restore():
    deck_id = create_deck()
    setup(deck_id)

    requests.get(f"https://api.countapi.xyz/hit/{deck_id}")
    data = {deck_id : {"room_name" : "The Room of Requirements", "counter" : f"https://api.countapi.xyz/get/{deck_id}", "game_finished" : "False", "player1_finished" : "False", "player2_finished" : "False"}}
    data = json.dumps(data)
    url = f"https://jsonblob.com/api/room/{blobId}"
    requests.put(url, data=data)

    # for testing the win screen
    deck_id = create_deck()
    hand1 = ""
    hand2 = ""
    cards = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=2").json()['cards']
    hand1 += cards[0]['code']
    hand2 += cards[1]['code']
    starting_card = draw_from_deck(deck_id)['code']
    requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/player1/add/?cards={hand1}")
    requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/player2/add/?cards={hand2}")
    requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/play/add/?cards={starting_card}")
    create_room(deck_id, "Insta win")

    # for testing the reshuffling cards
    # deck_id = create_deck()
    # hand1 = ""
    # hand2 = ""
    # cards = requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/draw/?count=50").json()['cards']
    # for i in range(25):
    #     hand1 += cards[i]['code'] + ","
    #     hand2 += cards[i + 25]['code'] + ","
    # starting_card = draw_from_deck(deck_id)['code']
    # requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/player1/add/?cards={hand1}")
    # requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/player2/add/?cards={hand2}")
    # requests.get(f"https://deckofcardsapi.com/api/deck/{deck_id}/pile/play/add/?cards={starting_card}")
    # create_room(deck_id, "1-card deck")

    print(url)

restore()