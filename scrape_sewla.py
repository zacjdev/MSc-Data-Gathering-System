import requests
from bs4 import BeautifulSoup
from classes import Event
from classes import Location
from geo import get_lat_long
import hashlib

# ---------- SEWLA Scraper ----------
def scrape_sewla_events():
    url = "https://www.sewla.org/events"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    events = []

    # Find the ul inside a div with sqs-block-content (multiple divs may exist)
    content_divs = soup.find_all("div", class_="sqs-block-content")
    for content_div in content_divs:
        event_list = content_div.find("ul")
        if event_list:
            break  # Stop after finding the first valid event list
    if not event_list:
        return events
    event_items = event_list.find_all("li")
    events = []
    for item in event_items:
        # Get the name from the <strong:> tag
        name = item.find("strong").get_text(strip=True) if item.find("strong") else None

        # Get the date from between "</strong: " and "<br>"
        date_text = item.get_text()
        # Split on ": "
        split_text = date_text.split(": ")
        date_text = split_text[1] if len(split_text) > 1 else date_text
        # Remove Host
        date_text_processed = date_text.split("Host")[0].strip()

        venue = split_text[-1].strip() if len(split_text) > 1 else None
        
        host = split_text[-2].strip() if len(split_text) > 2 else None
        if host:
            host = host.replace(" | Venue", "").strip()
        location = f"{venue} ({host})" if venue and host else venue or host

        # Get lat and long from the venue
        lat, long = get_lat_long(venue) if venue else (None, None)

        # Handle date ranges
        start_date = None
        end_date = None

        # Either in format "dd/mm/yyyy" or "dd and dd/mm/yyyy" convert to epoch
        from datetime import datetime
        if "TBC" in date_text_processed or "TBA" in date_text_processed:
            start_date = None
            end_date = None
        elif " and " in date_text_processed or " - " in date_text_processed:
            # split on " - " if it exists
            date_text_processed = date_text_processed.replace(" - ", " and ")
            # split on " and "
            date_split = date_text_processed.split(" and ")
            date_parts = date_split[1].split("/")
            # for start date use the first part for day ONLY and the second part for month and year
            start_date = datetime.strptime(f"{date_split[0]}/{date_parts[1]}/{date_parts[2]}", "%d/%m/%Y").timestamp()
            end_date = datetime.strptime(f"{date_parts[0]}/{date_parts[1]}/{date_parts[2]}", "%d/%m/%Y").timestamp()
     
        else:
            start_date = datetime.strptime(date_text_processed, "%d/%m/%Y").timestamp()
            end_date = start_date

        hash_input= f"{name}{url}"
        hash_object = hashlib.sha256(hash_input.encode()).hexdigest()

        # Instantiate Event object
        event = Event(
            name=name,
            dateText = date_text_processed,
            location=Location(
                description=f"Host: {host}" if host else None,
                address=venue,
                lat=lat,
                long=long,
                generatedCoords=True

            ),
            sourceUrl=url,
            dateStart=date_text_processed,
            sourceName="SEWLA",
            sport="Lacrosse",
            hash=hash_object
        )
        events.append(event)
    
    return events