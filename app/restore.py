import requests
import json
from deck import *
import deck
blobId = 1051631725620510720

def restore():
    deck_id = create_deck()
    setup(deck_id)

    requests.get(f"https://api.countapi.xyz/hit/{deck_id}")
    data = {deck_id : {"room_name" : "The Room of Requirements", "counter" : f"https://api.countapi.xyz/get/{deck_id}"}}
    data = json.dumps(data)
    url = f"https://jsonblob.com/api/room/{blobId}"
    requests.put(url, data=data)
    print(url)

restore()