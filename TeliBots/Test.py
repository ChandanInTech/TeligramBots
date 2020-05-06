import requests
from bs4 import BeautifulSoup as bs

sa_corona_url = 'https://en.wikipedia.org/wiki/COVID-19_pandemic_in_Texas'


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


print(corona_tx_cases_update())
