import json

import requests

token = "1240403795:AAHCKKtoNmrDWxOuxSxa4DgJD-S69PKhBLw"
base = "https://api.telegram.org/bot{}/".format(token)


def get_chat_ids():
    url = base + "getUpdates"
    r = requests.get(url)
    resp = json.loads(r.content).get('result')

    chat_ids = []

    for x in resp:
        chat_id = x.get('message').get('from').get('id')
        if chat_id not in chat_ids:
            chat_ids.append(chat_id)

    return chat_ids


print(get_chat_ids())
