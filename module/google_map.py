import os
import googlemaps
from datetime import datetime

# Initialize the client with your API key
API_KEY = os.environ['GOOGLE_MAP_API_KEY']

def get_near_restaurant(latitude: float, longitude: float, radius: int, keyword: str = "") -> str:
    gmaps = googlemaps.Client(key=API_KEY)

    # Define the location
    location = (latitude, longitude)  # Latitude and Longitude

    # Search for nearby restaurants
    places_result = gmaps.places_nearby(location=location, radius=radius, type="restaurant", keyword = keyword)

    msg = ""
    # Display the results
    for place in places_result['results']:
        msg += f"{place['name']}\n"
        msg += f"Address: {place.get('vicinity', 'N/A')}\n"
        msg += f"Rating: {place.get('rating', 'N/A')} (from {place.get('user_ratings_total', 0)} reviews)\n\n"
    
    return msg