import requests
import json
import time

from TeliBots import Private
from TeliBots.CoronaCases import CoronaCases

token = Private.token
chat_id = Private.chat_id
chat_id_p = Private.chat_id_p

base = f"https://api.telegram.org/bot{token}/"

corona_cases = CoronaCases()


def get_updates():
    url = base + "getUpdates?timeout=100"
    r = requests.get(url)
    return json.loads(r.content)


def send_message(message_text, c_chat_id):
    url = base + f"sendMessage?text={message_text}&chat_id={c_chat_id}"
    requests.get(url)


count = 0
temp_cases = 0
temp_deaths = 0
temp_recovered = 0
temp_sa_count = 0
while True:
    update_time = corona_cases.get_corona_updates()[0]
    updated_cases = corona_cases.get_corona_updates()[1]
    updated_deaths = corona_cases.get_corona_updates()[2]
    updated_recovered = corona_cases.get_corona_updates()[3]
    updated_sa_count = corona_cases.corona_sa_cases_update()

    if temp_cases != updated_cases or temp_deaths != updated_deaths or temp_recovered != updated_recovered or temp_sa_count != updated_sa_count:
        print(count, update_time, updated_cases, updated_deaths, updated_recovered)
        send_message(
            f"Cases: {updated_cases}\nDeaths: {updated_deaths}\nRecovered: {updated_recovered}\nSan Antonio Cases: {updated_sa_count}",
            chat_id)
        send_message(
            f"Cases: {updated_cases}\nDeaths: {updated_deaths}\nRecovered: {updated_recovered}\nSan Antonio Cases: {updated_sa_count}",
            chat_id_p)
        temp_cases = updated_cases
        temp_recovered = updated_recovered
        temp_deaths = updated_deaths
        temp_sa_count = updated_sa_count
    count += 1
    time.sleep(60 * 5)
