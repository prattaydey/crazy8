import requests
import json
blobId = 1051631725620510720

def restore():
    data = {"not_a_real_id" : "not_a_real_room"}
    data = json.dumps(data)
    url = f"https://jsonblob.com/api/room/{blobId}"
    requests.put(url, data=data)

restore()