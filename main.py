from src.scraper import WikipediaScraper

def main():
    scraper = WikipediaScraper()
    countries = scraper.get_countries()
    print(countries)

    leader = scraper.get_leaders(countries)
    print([leader])

if __name__ == "__main__":
    main()
