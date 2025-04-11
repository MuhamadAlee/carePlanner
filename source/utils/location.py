from geopy.geocoders import Nominatim
from geopy.distance import geodesic  
from math import radians, sin, cos, sqrt, atan2
from datetime import datetime, timedelta

geolocator = Nominatim(user_agent="my_geocoder")

def find_coordinates(location):
    location = geolocator.geocode(location)  
    return location.latitude, location.longitude

def get_distance(loc1, loc2):
    """Calculate the geographical distance between two locations."""
    return geodesic(loc1, loc2).km

def get_distance_in_miles(loc1, loc2):
    """Calculate the geographical distance between two locations."""
    return geodesic(loc1, loc2).mi


def estimate_travel_time(start_location, end_location, reaching_time_str):
    """
    Estimate travel time given start and end locations with reaching time.
    
    Parameters:
    - start_location: tuple (latitude, longitude)
    - end_location: tuple (latitude, longitude)
    - reaching_time_str: str (format: "HH:MM", 24-hour format)

    Returns:
    - Estimated travel time in hours and minutes
    """
    # Convert reaching_time string to datetime object
    reaching_time_str = reaching_time_str.strftime("%H:%M")
    reaching_time = datetime.strptime(reaching_time_str, "%H:%M")
    
    # Calculate distance in km
    distance_km = geodesic(start_location, end_location).km

    # Estimate speed based on time of day
    if 7 <= reaching_time.hour < 10:
        estimated_speed = 30  # Morning rush
    elif 10 <= reaching_time.hour < 16:
        estimated_speed = 40  # Daytime
    elif 16 <= reaching_time.hour < 20:
        estimated_speed = 25  # Evening rush
    else:
        estimated_speed = 50  # Nighttime

    # Calculate estimated travel time (in hours)
    travel_time_hours = distance_km / estimated_speed
    travel_time_minutes = travel_time_hours * 60

    return round(travel_time_hours, 2)