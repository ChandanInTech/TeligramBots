from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs


class CoronaCases:
    corona_url = "https://www.worldometers.info/coronavirus/country/us/"

    def get_corona_updates(self):

        page = requests.get(self.corona_url)
        soup = bs(page.content, 'html.parser')

        all_numbers = soup.find_all('div', class_='maincounter-number')

        us_cases = all_numbers[0].get_text().strip()
        us_deaths = all_numbers[1].get_text().strip()
        us_recovered = all_numbers[2].get_text().strip()

        return [datetime.now().strftime("%d/%m/%Y %H:%M:%S"), us_cases, us_deaths, us_recovered, all_numbers]
