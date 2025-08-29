from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time

# Function to get latitude and longitude for a given place name - Uses Nominatim (OpenStreetMap) geocoding service with basic retry logic
def get_lat_long(place_name, retries=3, delay=1):
    print(f"Getting lat/long for: {place_name} (Warning: Rate limited)")

    if not place_name or any(x in place_name.upper() for x in ["TBC", "TBA"]):
        return None, None

    geolocator = Nominatim(user_agent="msc-lax-scraper")

    for attempt in range(retries):
        try:
            location = geolocator.geocode(place_name, timeout=5)
            if location:
                print(f"Found lat/long for {place_name}: {location.latitude}, {location.longitude}")
                return location.latitude, location.longitude
            else:
                print(f"No result for '{place_name}'")
                return None, None
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            print(f"Geocoder error on attempt {attempt+1}/{retries} for '{place_name}': {e}")
            time.sleep(delay)

    print(f"Failed to get lat/long for '{place_name}' after {retries} attempts.")
    return None, None
