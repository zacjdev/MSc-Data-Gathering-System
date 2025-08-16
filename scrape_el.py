import requests
from bs4 import BeautifulSoup
from classes import Event
from classes import Location
from geo import get_lat_long
import hashlib

def scrape_el():
    url = "https://www.englandlacrosse.co.uk/events-1"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    events = []

    # Find all event containers
    event_containers = soup.find_all("article", class_="eventlist-event")

    for container in event_containers:
        # Title
        title_tag = container.find("h1", class_="eventlist-title")
        name = title_tag.get_text(strip=True) if title_tag else None

        # Date
        date_tag = container.find_all("li", class_="eventlist-meta-date")[0]
        # get the first <span> tag inside the date li as it contains the date in the datetime field and the time in the text
        start_date_span = date_tag.find("span") if date_tag else None
        # decide if the li tag has a span inside it

        if start_date_span:
            ### events over multiple days
            #get the first time tag inside the span
            date_timetags = container.find_all("time", class_="event-time-12hr") if start_date_span else None

            start_date_timetag = date_timetags[0] if date_timetags else None


            start_date_date = start_date_timetag.get("datetime") if start_date_span else None
            start_date_text = start_date_timetag.get_text(strip=True) if start_date_span else None

            # get the second <span> tag inside the date li for end date and time
            end_date_timetag = date_timetags[1] if len(date_timetags) > 1 else None
            end_date_date = end_date_timetag.get("datetime") if end_date_timetag else None
            end_date_text = end_date_timetag.get_text(strip=True) if end_date_timetag else None


        else:
            ### events on a single day
            start_date_timetag = date_tag.find("time") if date_tag else None
            start_date_date = start_date_timetag.get("datetime") if start_date_timetag else None
            end_date_date = start_date_date
            times_li = container.find("li", class_="eventlist-meta-time") if container else None
            # get the time tags inside the times li
            start_time_tag = times_li.find("time", class_="event-time-12hr-start") if times_li else None
            start_date_text = start_time_tag.get_text(strip=True) if start_time_tag else None
            end_time_tag = times_li.find("time", class_="event-time-12hr-end") if times_li else None
            end_date_text = end_time_tag.get_text(strip=True) if end_time_tag else None
        
        # Combine date and time into an epoch int
        from datetime import datetime
        dateStart = int(datetime.fromisoformat(start_date_date).timestamp()) if start_date_date else None
        dateEnd = int(datetime.fromisoformat(end_date_date).timestamp()) if end_date_date else None        


        # Location
        location_tag = container.find("li", class_="eventlist-meta-address")

        # strip text from the li, then explopre the a tag and get the href
        location = location_tag.get_text(strip=True) if location_tag else None
        # remove (map) from the location text
        if location:
            location = location.replace("(map)", "").strip()
        if location_tag and location_tag.a:
            address = location_tag.a.get("href")
            # remove the http://maps.google.com?q=
            address = address.replace("http://maps.google.com?q=", "")
        else:
            # if no address is found, set it to None
            address = None

        # Description
        desc_tag = container.find("div", class_="eventlist-description")
        description = desc_tag.get_text(strip=True) if desc_tag else None

        # Category
        category_tag = container.find("div", class_="eventlist-cats")
        # go to a tag inside category div
        category = category_tag.find("a").get_text(strip=True) if category_tag else None

        sourceUrl = url

        # get lat and long from the address
        lat, long = get_lat_long(address) if address else (None, None)

        hash_input= f"{name}{sourceUrl}{dateStart}{dateEnd}"

        hash_object = hashlib.sha256(hash_input.encode()).hexdigest()

        # Create Event instance
        event = Event(
            name=name,
            dateStart=dateStart,
            dateEnd=dateEnd,
            location= Location(
                address=address,
                description=description,
                lat=lat,
                long=long,
                generatedCoords=True

            ),
            description=description,
            category=category,
            sourceUrl=sourceUrl,
            sourceName="England Lacrosse",
            sport="Lacrosse",
            hash =hash_object,
        )

        events.append(event)

    return events