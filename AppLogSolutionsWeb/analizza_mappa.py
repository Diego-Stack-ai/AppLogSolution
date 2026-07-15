import sys
import json
import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate("functions/log-solutions-sviluppo-firebase-adminsdk-z1qov-34d28af04b.json")
firebase_admin.initialize_app(cred)

bucket = storage.bucket(name="log-solutions-sviluppo.firebasestorage.app")
data_consegna = "2026-07-09"

print("Scaricando i viaggi correnti...")
blob_old = bucket.blob(f"REPORTS/{data_consegna}/viaggi_giornalieri_Johnson.json")
if not blob_old.exists():
    print("Mappa non trovata in REPORTS!")
    sys.exit(1)

mappa = json.loads(blob_old.download_as_string().decode('utf-8'))
zone = mappa.get("zone", [])

nuovi_arrivi = []
altre_zone = []

for z in zone:
    if z.get("id_zona") == "DDT_DA_INSERIRE":
        nuovi_arrivi = z.get("lista_punti", [])
    elif z.get("id_zona") not in ("0000", "SENZA_ZONA"):
        altre_zone.append(z)

print(f"Zone calcolate: {len(altre_zone)}")
for z in altre_zone:
    print(f"- {z.get('nome_giro')} ({z.get('id_zona')}): {len(z.get('lista_punti', []))} punti. Stato: {z.get('_stato', 'bozza')}")

print(f"\nNuovi arrivi: {len(nuovi_arrivi)} punti")
if nuovi_arrivi:
    print("Primi 5 Nuovi Arrivi:")
    for p in nuovi_arrivi[:5]:
        print(f"  - {p.get('codice_frutta')} / {p.get('codice_latte')} / {p.get('nome')}")
