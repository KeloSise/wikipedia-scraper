# scraper.py

import requests
from bs4 import BeautifulSoup
import json

class WikipediaScraper:
    def __init__(self):
        self.base_url = "https://country-leaders.onrender.com"
        self.country_endpoint = "/countries"
        self.leaders_endpoint = "/leaders"
        self.cookies_endpoint = "/cookie"
        self.leaders_data = {}
        self.cookie = self.refresh_cookie()

    def refresh_cookie(self):
        # Refreshes cookie and returns it
        cookie_response = requests.get(self.base_url + self.cookies_endpoint)
        return cookie_response.cookies

    def get_countries(self):
        # Retrieves a list of countries
        countries_response = requests.get(self.base_url + self.country_endpoint, cookies=self.cookie)
        return countries_response.json()

    def get_leaders(self, country):
        # Retrieves leaders for a specific country
        leader_details = []
        country_list = self.get_countries()
        if not country_list:
            print("No countries found. Exiting.")
            return leader_details
        for country in country_list:
            params = {'country': country}
            leader_response = requests.get(f"{self.base_url}{self.leaders_endpoint}", cookies=self.cookie, params=params)
            if leader_response.status_code == 200:
                leader_details.append(leader_response.text)
            else:
                print(f"Failed to fetch leaders for {country}. Status code: {leader_response.status_code}")
        return leader_details

    def get_first_paragraph(self, wikipedia_url):        
        wikipedia_response = requests.get(wikipedia_url)
        soup = BeautifulSoup(wikipedia_response.text, 'html.parser')
        first_paragraph = soup.find('p').get_text()
        return first_paragraph
        pass
        

    def to_json_file(self, filepath):
        # Saves data structure into a JSON file
        with open(filepath, 'w') as json_file:
            json.dump(self.leaders_data, json_file)
            pass

  
