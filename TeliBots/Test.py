import json
import csv
import requests

token = "1240403795:AAHCKKtoNmrDWxOuxSxa4DgJD-S69PKhBLw"
base = "https://api.telegram.org/bot{}/".format(token)

csv_file = "chat_ids.csv"

chat_ids = []


# def get_chat_ids():
#     url = base + "getUpdates"
#     r = requests.get(url)
#     resp = json.loads(r.content).get('result')
#
#     chat_ids = []
#
#     for x in resp:
#         chat_id = x.get('message').get('from').get('id')
#         if chat_id not in chat_ids:
#             chat_ids.append(chat_id)
#
#     return chat_ids


def get_chat_ids_csv():
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        row = next(reader)
        for x in row:
            if int(x) not in chat_ids:
                chat_ids.append(int(x))


def update_csv():
    with open(csv_file, 'w', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(chat_ids)


# update_csv()
get_chat_ids_csv()
print(chat_ids)
