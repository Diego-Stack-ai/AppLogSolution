import requests
import os
import json

API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY")

# A set of coordinates
pts = [
    "45.442805,11.714498", # 0
    "45.443805,11.715498", # 1
    "45.444805,11.716498", # 2
    "45.445805,11.717498", # 3
    "45.446805,11.718498", # 4
    "45.447805,11.719498", # 5
    "45.448805,11.720498", # 6
    "45.449805,11.721498", # 7
    "45.450805,11.722498", # 8
    "45.451805,11.723498", # 9
    "45.452805,11.724498", # 10
    "45.453805,11.725498", # 11
    "45.454805,11.726498", # 12
]

def test_chunk(chunk_size):
    sub = pts[:chunk_size+1]
    origin = sub[0]
    dest = sub[-1]
    waypts = "|".join(sub[1:-1])
    
    url = (f"https://maps.googleapis.com/maps/api/directions/json"
           f"?origin={origin}&destination={dest}"
           f"&waypoints={waypts}&key={API_KEY}")
           
    print(f"\n--- Testing CHUNK={chunk_size} (Waypoints: {len(sub[1:-1])}) ---")
    r = requests.get(url).json()
    print("Status:", r.get("status"))
    if r.get("status") != "OK":
        print("Error message:", r.get("error_message"))

if not API_KEY:
    print("No API KEY found!")
else:
    test_chunk(8)
    test_chunk(9)
    test_chunk(10)
    test_chunk(11)
