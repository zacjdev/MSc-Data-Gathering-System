import json
# import functions
from scrape_el import scrape_el
from scrape_semla import get_clubs
from scrape_semla import scrape_individual_club
from scrape_semla import get_fixtures
from scrape_semla import get_clubs_api_names
from scrape_sewla import scrape_sewla_events
import requests
from classes import Event, Club, Game
from geopy.geocoders import Nominatim

# Control which scrapers to run
modules = {
    "el": True,  # England Lacrosse}
    "semla": False, # SEMLA (South Mens)
    "sewla": False, # SEWLA (South Womens)
}

def scrape_data():
    el_events = []
    if modules["el"]:
        el_events = scrape_el()
        print(f"Scraped {len(el_events)} events from England Lacrosse.")

    semla_clubs = []
    if modules["semla"]:
        semla_clubs = get_clubs()
    semla_clubs_full = []
    semla_fixtures_full = []
    club_fixtures = []
    if modules["semla"] and semla_clubs:
        for club in semla_clubs:
            semla_clubs_full.append(scrape_individual_club(club['link'], club['name']))

        semla_clubs_api_names = get_clubs_api_names()
        for club in semla_clubs_api_names:
            club_fixtures.append(get_fixtures(club, semla_clubs_full))
            for club in club_fixtures:
                for game in club:
                    semla_fixtures_full.append(game)
    sewla_events = []
    if modules["sewla"]:
        sewla_events = scrape_sewla_events()

    print(f"Scraped {len(semla_clubs_full)} clubs from SEMLA.")
    print(f"Scraped {len(semla_fixtures_full)} fixtures from SEMLA.")
    print(f"Scraped {len(sewla_events)} events from SEWLA.")

    events = el_events + sewla_events
    games = semla_fixtures_full

    clubs = semla_clubs_full

    return {
        "games": games,
        "events": events,
        "clubs": clubs
    }
import json

def convert(obj_list):
    def serialize(obj):
        if hasattr(obj, "to_dict"):
            return {k: serialize(v) for k, v in obj.to_dict().items()}
        elif isinstance(obj, dict):
            return {k: serialize(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [serialize(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(serialize(item) for item in obj)
        elif isinstance(obj, (str, int, float, bool)) or obj is None:
            return obj
        else:
            raise TypeError(f"Cannot serialize object of type {type(obj)}: {obj}")

    converted = [serialize(obj) for obj in obj_list]

    # Remove duplicates using JSON serialization (handles nested dicts)
    seen = set()
    unique = []
    for item in converted:
        item_str = json.dumps(item, sort_keys=True)
        if item_str not in seen:
            seen.add(item_str)
            unique.append(item)

    return unique

def post_data(collection_name, data):
    url = f"http://localhost:3000/api/{collection_name}"
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print(f"{collection_name} data saved successfully.")
    else:
        print(f"Failed to save {collection_name}. Status code: {response.status_code}")
        print(response.text)

        
def main():
    data = scrape_data()
    ser_games = convert(data["games"])
    print(f"Converted {len(ser_games)} games to serializable format.")

    ser_events = convert(data["events"])
    ser_clubs = convert(data["clubs"])

    if ser_events and len(ser_events) > 0:
        post_data("events", ser_events)
    else:
        print("No events to post.")

    if ser_games and len(ser_games) > 0:
        post_data("games", ser_games)
    else:
        print("No games to post.")

    if ser_clubs and len(ser_clubs) > 0:
        post_data("clubs", ser_clubs)
    else:
        print("No clubs to post.")


if __name__ == "__main__":
    main()
