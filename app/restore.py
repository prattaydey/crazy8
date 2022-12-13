import requests
import json
blobId = 1051631725620510720

def restore():
    data = {"not_a_real_id" : {"room_name" : "not_a_real_room", "player1" : "not_a_real_player", "player2" : "not_a_real_player"}}
    data = json.dumps(data)
    url = f"https://jsonblob.com/api/room/{blobId}"
    requests.put(url, data=data)
    print(url)

restore()