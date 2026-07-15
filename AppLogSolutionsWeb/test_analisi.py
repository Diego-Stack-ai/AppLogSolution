import sys
sys.path.append('functions')
import main
from firebase_admin import storage
import json

main.initialize_firebase_if_needed()
bucket = storage.bucket(name="log-solutions-sviluppo.appspot.com") # Sviluppo bucket
blob = bucket.blob("REPORTS/2026-07-09/viaggi_giornalieri_Johnson.json")
if blob.exists():
    data = json.loads(blob.download_as_string().decode('utf-8'))
    zone = data.get("zone", [])
    print(f"File found. Totale zone: {len(zone)}")
    for z in zone:
        print(f"- {z.get('nome_giro')} (id: {z.get('id_zona')}): {len(z.get('lista_punti', []))} punti")
else:
    print("File not found in storage")
