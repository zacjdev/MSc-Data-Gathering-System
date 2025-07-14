import requests
from bs4 import BeautifulSoup
from classes import Event

def scrape_sewla_events():
    url = "https://www.sewla.org/events"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    events = []
    print(f"Scraping events from {url}")

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
        # get the name from the <strong:> tag
        name = item.find("strong").get_text(strip=True) if item.find("strong") else None

        # get the date from between "</strong: " and "<br>"
        date_text = item.get_text()
        # split on ": "
        split_text = date_text.split(": ")
        date_text = split_text[1] if len(split_text) > 1 else date_text
        # remove Host
        date_text_processed = date_text.split("Host")[0].strip()

        venue = split_text[-1].strip() if len(split_text) > 1 else None
        # remove  # remove  | Venue  from the venue if it exists
        
        host = split_text[-2].strip() if len(split_text) > 2 else None
        if host:
            host = host.replace(" | Venue", "").strip()
        location = f"{venue} ({host})" if venue and host else venue or host

        event = Event(
            name=name,
            dateText = date_text_processed,
            location=location,
            sourceUrl=url,
            sourceName="SEWLA",
        )
        events.append(event)
    
    return events


        
        