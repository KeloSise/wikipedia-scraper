from src.scraper import WikipediaScraper

def main():
    scraper = WikipediaScraper()
    countries = scraper.get_countries()
    print(countries)

    leader_data = scraper.get_leaders(countries)
    print(leader_data)

if __name__ == "__main__":
    main()
