import os
import requests
from dotenv import load_dotenv

load_dotenv () 
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def fetch_traffic(origin, destination):
    endpoint = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,  # You can customize this
        "departure_time": "now",
        "traffic_model": "best_guess",
        "mode": "driving",
        "key": GOOGLE_API_KEY
    }

    response = requests.get(endpoint, params=params)
    data = response.json()

    if data.get("status") == "OK":
        duration = data["routes"][0]["legs"][0]["duration_in_traffic"]["text"]
        return f"Estimated travel time: {duration}"
    else:
        return f"Error fetching traffic: {data.get('status')}"
