import requests
import json
from deck import *
import deck
blobId = 1051631725620510720

def restore():
    deck_id = create_deck()
    setup(deck_id)

    data = {deck_id : {"room_name" : "The Room of Requirements", "player1" : "not_a_real_player"}}
    data = json.dumps(data)
    url = f"https://jsonblob.com/api/room/{blobId}"
    requests.put(url, data=data)
    print(url)

restore()