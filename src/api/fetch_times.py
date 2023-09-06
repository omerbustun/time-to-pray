import json
import os
import requests
from datetime import datetime, timedelta

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "config", "settings.json")

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data")

API_URL_MONTHLY = "http://api.aladhan.com/v1/calendarByCity/{year}/{month}"

API_URL_DAILY = "http://api.aladhan.com/v1/timingsByCity"

METHODS = {
    "Muslim World League": 3,
    "Islamic Society of North America (ISNA)": 2,
    "Egyptian General Authority of Survey": 5,
    "Umm Al-Qura University, Makkah": 4,
    "University of Islamic Sciences, Karachi": 1,
    "Institute of Geophysics, University of Tehran": 7,
    "Shia Ithna-Ashari, Leva Institute, Qum": 0,
    "Gulf Region": 8,
    "Kuwait": 9,
    "Qatar": 10,
    "Majlis Ugama Islam Singapura, Singapore": 11,
    "Union Organization Islamic de France": 12,
    "Diyanet İşleri Başkanlığı, Turkey": 13,
    "Spiritual Administration of Muslims of Russia": 14,
    "Moonsighting Committee Worldwide (Moonsighting.com)": 15,
    "Dubai (experimental)": 16
}

def read_config():
    """Read configurations from settings.json."""
    if not os.path.exists(CONFIG_PATH):
        return {}

    with open(CONFIG_PATH, 'r') as file:
        return json.load(file)

def write_config(data):
    """Write configurations to settings.json."""
    with open(CONFIG_PATH, 'w') as file:
        json.dump(data, file, indent=4)

def fetch_monthly_prayer_times(month, year, country="Turkey", city="Istanbul", method="13"):
    """Fetch prayer times from Aladhan API for a given city, country, month, and year."""
    endpoint = API_URL_MONTHLY.format(year=year, month=month)

    params = {
        "city": city,
        "country": country,
        "method": method
    }

    response = requests.get(endpoint, params=params)
    if response.status_code != 200:
        return None

    data = response.json()
    if "data" in data:
        monthly_data = [day["timings"] for day in data["data"]]
        with open(os.path.join(DATA_DIR, f"prayer_times_{year}_{month}.json"), 'w') as file:
            json.dump(monthly_data, file, indent=4)
        return monthly_data
    return None

def validate_location(city, country, method="13"):
    """Validate if the provided city and country are recognized by the API."""
    
    params = {
        "city": city,
        "country": country,
        "method": method
    }
    
    response = requests.get(API_URL_DAILY, params=params)
    data = response.json()
    if response.status_code == 200 and "data" in data and "meta" in data["data"]:
        latitude = data["data"]["meta"]["latitude"]
        longitude = data["data"]["meta"]["longitude"]
        return str(latitude), str(longitude)

    return None, None

def get_monthly_prayer_times():
    config = read_config()
    city = config.get("city", "Istanbul")
    country = config.get("country", "Turkey")
    method = config.get("method", "13")

    # Get current month and year
    current_date = datetime.now()
    month = current_date.month
    year = current_date.year

    # Check if data for the current month is stored locally
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    file_path = os.path.join(DATA_DIR, f"prayer_times_{year}_{month}.json")
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            stored_data = json.load(file)
    else:
        # Fetch monthly prayer times if not stored locally
        stored_data = fetch_monthly_prayer_times(month, year, country, city, method)

    # Return prayer times for the current day
    return stored_data[current_date.day - 1] if stored_data else None

def get_remaining_time_for_next_prayer(prayer_times):
    """
    Returns the remaining time for the next prayer.
    
    Args:
    - prayer_times (dict): Dictionary containing the prayer times for a specific day.
    
    Returns:
    - tuple: (name_of_next_prayer, remaining_time)
    """
    now = datetime.now().time()
    next_prayer = None
    remaining_time = None

    # List of prayers in order
    prayers = ["Fajr", "Dhuhr", "Asr", "Maghrib", "Isha"]
    
    for prayer in prayers:
        time_str = prayer_times[prayer].split(" ")[0]  # Get only the "04:53" part, ignoring the timezone offset
        prayer_time = datetime.strptime(time_str, '%H:%M').time()
        if now < prayer_time:
            next_prayer = prayer
            # Calculate remaining time
            current_time_in_minutes = now.hour * 60 + now.minute
            prayer_time_in_minutes = prayer_time.hour * 60 + prayer_time.minute
            remaining_minutes = prayer_time_in_minutes - current_time_in_minutes
            remaining_time = timedelta(minutes=remaining_minutes)
            break

    return next_prayer, remaining_time
