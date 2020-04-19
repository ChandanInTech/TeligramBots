import json
import requests
import time
from bs4 import BeautifulSoup as bs

token = "1240403795:AAHCKKtoNmrDWxOuxSxa4DgJD-S69PKhBLw"
corona_url = "https://www.worldometers.info/coronavirus/country/us/"
sa_corona_url = "https://www.ksat.com/news/local/2020/03/17/heres-what-we-know-about-the-4-confirmed-covid-19-cases-in-san-antonio/"

chat_ids = []

base = "https://api.telegram.org/bot{}/".format(token)


def get_corona_updates():
    page = requests.get(corona_url)
    soup = bs(page.content, 'html.parser')

    all_numbers = soup.find_all('div', class_='maincounter-number')

    us_cases = all_numbers[0].get_text().strip()
    us_deaths = all_numbers[1].get_text().strip()
    us_recovered = all_numbers[2].get_text().strip()

    return [us_cases, us_deaths, us_recovered]


def corona_sa_cases_update():
    page = requests.get(sa_corona_url)
    soup = bs(page.content, 'html.parser')

    sa_cc = soup.find_all('h1', class_="headline")

    sa_count = sa_cc[0].get_text()

    return sa_count.split()[0]


def send_message(message_text):
    get_chat_ids()
    for chat_id in chat_ids:
        url = base + "sendMessage?text={}&chat_id={}".format(message_text, chat_id)
        requests.get(url)


def get_chat_ids():
    url = base + "getUpdates"
    r = requests.get(url)
    resp = json.loads(r.content).get('result')

    chat_ids.clear()

    for x in resp:
        chat_id = x.get('message').get('from').get('id')
        if chat_id not in chat_ids:
            chat_ids.append(chat_id)

    return chat_ids


count = 0
temp_cases = 0
temp_deaths = 0
temp_recovered = 0
temp_sa_count = 0

while True:
    updated_cases = get_corona_updates()[0]
    updated_deaths = get_corona_updates()[1]
    updated_recovered = get_corona_updates()[2]
    updated_sa_count = corona_sa_cases_update()

    if temp_cases != updated_cases \
            or temp_deaths != updated_deaths \
            or temp_recovered != updated_recovered \
            or temp_sa_count != updated_sa_count:
        print(count, updated_cases, updated_deaths, updated_recovered, updated_sa_count)

        message_text = "US Cases: {}\nUS Deaths: {}\nUS Recovered: {}\nSan Antonio Cases: {}".format(updated_cases,
                                                                                                     updated_deaths,
                                                                                                     updated_recovered,
                                                                                                     updated_sa_count)

        send_message(message_text)

        temp_cases = updated_cases
        temp_recovered = updated_recovered
        temp_deaths = updated_deaths
        temp_sa_count = updated_sa_count

    count += 1
    time.sleep(60 * 30)
