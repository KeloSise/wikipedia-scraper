from src.scraper import WikipediaScraper

def main():
    scraper = WikipediaScraper()
    countries = scraper.get_countries()
    print(countries)

    leader_data = scraper.get_leaders(countries)
    scraper.print_leaders(leader_data)

    leader_output_filepath = "leader_output.json"
    scraper.to_json_file(leader_output_filepath)
    print(f"Updated leaders data saved to {leader_output_filepath}")


if __name__ == "__main__":
    main()
