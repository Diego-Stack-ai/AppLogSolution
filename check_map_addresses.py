import os
import glob
import re
import urllib.parse
import urllib.request
import json

HTML_DIR = r"G:\Il mio Drive\AppLogSolutions\Fatturazione\Mappe_Complete_Google\marzo 2026"
API_KEY = "AIzaSyAHQ3HjuEEIS8bn5KMh6N3UoM6kZ2MYGL4"

def check_address(address):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={urllib.parse.quote(address)}&key={API_KEY}"
    try:
        req = urllib.request.urlopen(url)
        res = json.loads(req.read())
        if res['status'] == 'OK':
            loc_type = res['results'][0]['geometry']['location_type']
            if loc_type == 'APPROXIMATE':
                return "APPROSSIMATIVO (trovata solo zona o citta')"
            return "OK"
        else:
            return res['status']
    except Exception as e:
        return str(e)

def main():
    files = glob.glob(os.path.join(HTML_DIR, "*.html"))
    all_addresses = set()

    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        matches = re.finditer(r'"wa":\s*"([^"]+)"', content)
        for m in matches:
            wa_link = m.group(1)
            url_parsed = urllib.parse.urlparse(wa_link)
            query = urllib.parse.parse_qs(url_parsed.query)
            waypoints_str = query.get('waypoints', [''])[0]
            if waypoints_str:
                waypoints = waypoints_str.split('|')
                for wp in waypoints:
                    all_addresses.add(urllib.parse.unquote(wp))

    print(f"Totale indirizzi unici trovati: {len(all_addresses)}")

    not_found = []
    approximate = []

    count = 0
    for wp in all_addresses:
        count += 1
        if count % 50 == 0:
            print(f"Progresso: {count}/{len(all_addresses)}...")
        status = check_address(wp)
        if status == "OK":
            continue
        elif "APPROSSIMATIVO" in status:
            approximate.append((wp, status))
        else:
            not_found.append((wp, status))

    print("\n--- INDIRIZZI NON TROVATI (ERRORI API) ---")
    for wp, st in not_found:
        print(f"'{wp}': {st}")

    print(f"\n--- INDIRIZZI APPROSSIMATIVI ---")
    for wp, st in approximate:
        print(f"'{wp}': {st}")

if __name__ == "__main__":
    main()
