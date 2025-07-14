import json
# import functions
from scrape_el import scrape_el
from scrape_semla import get_clubs
from scrape_semla import scrape_individual_club
from scrape_semla import get_fixtures
from scrape_semla import get_clubs_api_names
from scrape_sewla import scrape_sewla_events

def main():
    el_events = []
    el_events = scrape_el()
    print(f"Scraped {len(el_events)} events from England Lacrosse.")

    semla_clubs = get_clubs()
    semla_clubs_full = []
    semla_fixtures_full = []
    club_fixtures = []
    for club in semla_clubs:
        semla_clubs_full.append(scrape_individual_club(club['link'], club['name']))

    semla_clubs_api_names = get_clubs_api_names()
    for club in semla_clubs_api_names:
        club_fixtures.append(get_fixtures(club))
    #for club in club_fixtures:
        for game in club:
           semla_fixtures_full.append(game)
           
    sewla_events = scrape_sewla_events()
    print(f"Scraped {len(semla_clubs_full)} clubs from SEMLA.")
    print(f"Scraped {len(semla_fixtures_full)} fixtures from SEMLA.")
    print(f"Scraped {len(sewla_events)} events from SEWLA.")
    



if __name__ == "__main__":
    main()
