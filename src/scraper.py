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
        print("These are the countries retrieved from the API.")
        return countries_response.json()

    def get_leaders(self, country_list):
        # Retrieves leaders for a list of countries
        leaders_data = {}

        if not country_list:
            print("No countries found. Exiting the program.")
            return leaders_data

        for country in country_list:
            params = {'country': country}
            leader_response = requests.get(f"{self.base_url}{self.leaders_endpoint}", cookies=self.cookie, params=params)

            print(f"The request for {country}: gave HTTP response {leader_response.status_code}")

            if leader_response.status_code == 200:
                leaders_data[country] = leader_response.json()

        return leaders_data

    def print_leaders(self, leaders_data):
        # Retrieves a list of leaders and prints ID, Full Name
        for country, leaders in leaders_data.items():
            print(f"\nThese are the leaders retrieved for {country}:\n")
            for leader in leaders:
                print(f"Leader ID: {leader['id']}")
                print(f"  First Name: {leader['first_name']}")
                print(f"  Last Name: {leader['last_name']}")
                print(f"  Wikipedia URL: {leader['wikipedia_url']}")
                
                wikipedia_url = leader['wikipedia_url']
                first_paragraph = self.fetch_wikipedia_paragraph(wikipedia_url)

                if first_paragraph:
                    print(f"  First Paragraph: {first_paragraph}\n")
                    # Add the first paragraph to the leader details
                    leader['first_paragraph'] = first_paragraph
                else:
                    print("  Unable to fetch the first paragraph.\n")

        return leaders_data

    def fetch_wikipedia_paragraph(self, wikipedia_url):
        # Fetches the first paragraph from Wikipedia
        try:
            response = requests.get(wikipedia_url)
            response.raise_for_status()  
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')

            if paragraphs:
                return paragraphs[0].text.strip()

            print(f"No paragraphs found for {wikipedia_url}")
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from {wikipedia_url}: {e}")
            return None
        

    def to_json_file(self, filepath):
        # Saves data structure into a JSON file
        with open(filepath, 'w') as json_file:
            json.dump(self.leaders_data, json_file)
            

  
""" # Test
if __name__ == "__main__":
    scraper = WikipediaScraper()
    countries = scraper.get_countries()
    print(countries)

    leader_data = scraper.get_leaders(countries)
    print(leader_data) """  