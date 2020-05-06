import json
import requests
import time
import csv
from bs4 import BeautifulSoup as bs

token = "1240403795:AAHCKKtoNmrDWxOuxSxa4DgJD-S69PKhBLw"
corona_url = "https://www.worldometers.info/coronavirus/country/us/"
sa_corona_url = 'https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Texas'
csv_file = "chat_ids.csv"

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


def corona_tx_cases_update():
    page = requests.get(sa_corona_url)
    soup = bs(page.content, 'html.parser')

    table = soup.find('div', class_='tp-container')
    table_rows = table.find('table').find_all('tr')

    bexar_data = []
    travis_data = []

    for row in table_rows:
        th = row.find('th')
        if th and th.find('a') and th.find('a').get('title') and 'Bexar' in th.find('a').get('title'):
            bexar_data = [i.text.strip() for i in row.find_all('td')]
        elif th and th.find('a') and th.find('a').get('title') and 'Travis' in th.find('a').get('title'):
            travis_data = [i.text.strip() for i in row.find_all('td')]
            break

    return bexar_data, travis_data


def send_message(message_text):
    get_chat_ids_network()
    for chat_id in chat_ids:
        url = base + "sendMessage?text={}&chat_id={}".format(message_text, chat_id)
        requests.get(url)


def get_chat_ids_network():
    url = base + "getUpdates"
    r = requests.get(url)
    resp = json.loads(r.content).get('result')

    for x in resp:
        chat_id = x.get('message').get('from').get('id')
        if chat_id not in chat_ids:
            if chat_id not in chat_ids:
                chat_ids.append(chat_id)

    update_csv()


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


count = 0
temp_cases = 0
temp_deaths = 0
temp_recovered = 0
temp_sa_count = 0

# Runs from here

get_chat_ids_csv()

while True:
    updated_cases = get_corona_updates()[0]
    updated_deaths = get_corona_updates()[1]
    updated_recovered = get_corona_updates()[2]

    updated_sa_count = corona_tx_cases_update()[0][0]
    updated_sa_deaths = corona_tx_cases_update()[0][1]
    updated_sa_recovered = corona_tx_cases_update()[0][2]

    updated_austin_count = corona_tx_cases_update()[1][0]
    updated_austin_deaths = corona_tx_cases_update()[1][1]
    updated_austin_recovered = corona_tx_cases_update()[1][2]

    if temp_cases != updated_cases \
            or temp_deaths != updated_deaths \
            or temp_recovered != updated_recovered \
            or temp_sa_count != updated_sa_count:
        message_text = "US Cases: {}\n" \
                       "US Deaths: {}\n" \
                       "US Recovered: {}\n\n" \
                       "Bexar Case: {}\n" \
                       "Bexar Deaths: {}\n" \
                       "Bexar Recovered: {}\n\n" \
                       "Travis Cases: {}\n" \
                       "Travis Deaths: {}\n" \
                       "Travis Recovered: {}".format(
            updated_cases,
            updated_deaths,
            updated_recovered,
            updated_sa_count,
            updated_sa_deaths,
            updated_sa_recovered,
            updated_austin_count,
            updated_austin_deaths,
            updated_austin_recovered
        )

        print(str(count) + '\n' + message_text)
        send_message(message_text)

        temp_cases = updated_cases
        temp_recovered = updated_recovered
        temp_deaths = updated_deaths
        temp_sa_count = updated_sa_count

    count += 1
    time.sleep(60 * 30)
