import requests
from bs4 import BeautifulSoup
from classes import Club
from classes import Game

def get_clubs():
    url = "https://www.southlacrosse.org.uk/clubs"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    clubs = []
    # Find all club containers - td with class "cl-club"
    club_containers = soup.find_all("td", class_="cl-club")
    # for each, extract the club name and link
    for container in club_containers:
        club_name_tag = container.find("a")
        if club_name_tag:
            link = club_name_tag.get("href")
            if link and not link.startswith("http"):
                link = "https://www.southlacrosse.org.uk" + link
            # link will be a span inside the a tag 
            name = club_name_tag.get_text(strip=True)
            clubs.append({"name": name, "link": link})
    return clubs

def scrape_individual_club(link, club_name):
    response = requests.get(link)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract the club's details
    clubName = soup.find("h1", class_="wp-block-post-title").get_text(strip=True) if soup.find("h1", class_="wp-block-post-title") else club_name
    
    logoUrl = soup.find("img", class_="club-icon-img")["src"] if soup.find("img", class_="club-icon-img") else None

    website_tag = soup.find("p", class_="wp-block-semla-website")
    website = website_tag.find("a")["href"] if website_tag and website_tag.find("a") else None

    social_links = soup.find_all("a", class_="wp-block-social-link-anchor")
    facebook = next((link["href"] for link in social_links if "facebook.com" in link["href"]), None)
    twitter = next((link["href"] for link in social_links if "twitter.com" in link["href"]), None)
    instagram = next((link["href"] for link in social_links if "instagram.com" in link["href"]), None)

    # get the location div
    location_div = soup.find("div", class_="wp-block-semla-location")
    if location_div:
        # first p text
        locationAddress = location_div.find("p").get_text(strip=True) if location_div.find("p") else None
        # all other p texts
        locationDescription = " ".join(p.get_text(strip=True) for p in location_div.find_all("p")[1:]) if len(location_div.find_all("p")) > 1 else None
        # get the hidden iframe for lat and long - get data-url attribute
        iframeurl = location_div.find("iframe")["data-url"] if location_div.find("iframe") else None
        if iframeurl:
            # https://www.google.com/maps/embed/v1/place?q=51.599630%2C-0.224820&zoom=15&key=AIzaSyBa9auLpZff0JAO8ULWM-yJfi8gRcmN3GI
            # remove everything before the q= and after the &key=
            coords = iframeurl.split("q=")[1].split("&zoom=")[0] if "&zoom=" in iframeurl else None
            if coords:
                lat, long = coords.split("%2C")
                locationLat = float(lat) if lat else None
                locationLong = float(long) if long else None
            else:
                locationLat = None
                locationLong = None



    club = Club(
        clubName=clubName,
        logoUrl=logoUrl,
        website=website,
        facebook=facebook,
        twitter=twitter,
        instagram=instagram,
        locationDescription=locationDescription,
        locationAddress=locationAddress,
        locationLat=locationLat,
        locationLong=locationLong,
        sourceUrl=link,
        sourceName="SEMLA"

    )
    return club


def get_clubs_api_names():
    url = "https://www.southlacrosse.org.uk/api/semla/v1/clubs"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    clubs = []
    # get each tr and the first td, get the text 
    club_rows = soup.find_all("tr")
    for row in club_rows:
        club_name_tag = row.find("td")
        if club_name_tag:
            club_name_link = club_name_tag.find("a")
            if club_name_link:
                # get href
                link = club_name_link.get("href")
                # get the href and only the name after /clubs/
                name = link.split("/clubs/")[1]
                clubs.append(name)
    return clubs


def get_fixtures(club_name):
    url = f"https://www.southlacrosse.org.uk/api/semla/v1/clubs/{club_name}/fixtures.json"
    response = requests.get(url)
    response.raise_for_status()
    fixtures = response.json()
    # parse json into fixture class objects
    games = []
    for fixture in fixtures:
        game = Game(
            homeTeamId=None,
            homeTeamName=fixture.get("home"),
            awayTeamId=None,
            awayTeamName=fixture.get("away"),
            score = fixture.get("result"),
            competitionName=fixture.get("competition"),
            competitionId=None,
            location=None,
        )
        games.append(game)
    return games
