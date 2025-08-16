import json
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Optional
import uvicorn
from apscheduler.schedulers.background import BackgroundScheduler
import requests

# Import your scraping logic
from scrape_el import scrape_el
from scrape_semla import get_clubs, scrape_individual_club, get_fixtures, get_clubs_api_names
from scrape_sewla import scrape_sewla_events
from classes import Event, Club, Game

# ---------- Scraper + Processing Logic ----------

def scrape_data(modules):
    el_events = []
    if modules.get("el"):
        el_events = scrape_el()
        print(f"Scraped {len(el_events)} events from England Lacrosse.")

    semla_clubs = []
    if modules.get("semla"):
        semla_clubs = get_clubs()
    semla_clubs_full = []
    semla_fixtures_full = []
    club_fixtures = []
    if modules.get("semla") and semla_clubs:
        for club in semla_clubs:
            semla_clubs_full.append(scrape_individual_club(club['link'], club['name']))

        semla_clubs_api_names = get_clubs_api_names()
        for club in semla_clubs_api_names:
            club_fixtures.append(get_fixtures(club, semla_clubs_full))
            for club in club_fixtures:
                for game in club:
                    semla_fixtures_full.append(game)

    sewla_events = []
    if modules.get("sewla"):
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

def main(modules: dict):
    # Clear all collections in Next.js via /api/admin/reset
    reset_url = "http://localhost:3000/api/admin/reset"
    reset_response = requests.post(reset_url)
    
    if reset_response.status_code == 200:
        print("Successfully reset clubs, events, and games.")
    else:
        print("Failed to reset collections.")
        print(reset_response.text)
        return  # stop if reset failed to prevent inserting into stale data


    data = scrape_data(modules)
    ser_games = convert(data["games"])
    ser_events = convert(data["events"])
    ser_clubs = convert(data["clubs"])

    if ser_events:
        post_data("events", ser_events)
    else:
        print("No events to post.")
    if ser_games:
        post_data("games", ser_games)
    else:
        print("No games to post.")
    if ser_clubs:
        post_data("clubs", ser_clubs)
    else:
        print("No clubs to post.")

# ---------- FastAPI Setup ----------

app = FastAPI()

class ScrapeOptions(BaseModel):
    el: Optional[bool] = True
    semla: Optional[bool] = True
    sewla: Optional[bool] = True

@app.post("/run-scraper")
async def run_scraper(options: ScrapeOptions):
    modules = {
        "el": options.el,
        "semla": options.semla,
        "sewla": options.sewla
    }
    main(modules)
    return {"status": "Scraper run started", "options": modules}

# ---------- Scheduler ----------

scheduler = BackgroundScheduler()

def scheduled_job():
    print("Running scheduled scraper with all modules enabled.")
    main({"el": True, "semla": True, "sewla": True})

scheduler.add_job(scheduled_job, 'cron', hour=0, minute=0)  # every day at midnight
scheduler.start()

# ---------- Run with: uvicorn main:app --reload ----------
import threading

def manual_input_loop():
    while True:
        user_input = input("Type 'run' to manually trigger the scraper: ").strip().lower()
        if user_input == 'run':
            print("Manual trigger received. Running scraper with all modules enabled...")
            main({"el": True, "semla": True, "sewla": True})
        else:
            print("Unknown command. Type 'run' to trigger the scraper.")

input_thread = threading.Thread(target=manual_input_loop, daemon=True)
input_thread.start()
