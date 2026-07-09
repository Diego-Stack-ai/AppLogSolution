import requests
import os

API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")
url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins=45.442805,11.714498&destinations=45.443805,11.715498&key={API_KEY}"
print("Testing Distance Matrix API...")
r = requests.get(url).json()
print("Status:", r.get("status"))
if r.get("status") != "OK":
    print("Error:", r.get("error_message"))
