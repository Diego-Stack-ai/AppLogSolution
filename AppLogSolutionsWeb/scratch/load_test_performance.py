import os
import sys
import time

sys.path.append(os.path.abspath(r'g:\Il mio Drive\App\AppLogSolutionsWeb\functions'))
import firebase_admin
from firebase_admin import credentials

try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(r'g:\Il mio Drive\App\AppLogSolutionsWeb\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json')
        firebase_admin.initialize_app(cred)
except:
    pass

import main

print("=== LOAD TEST PERFORMANCE ===")

# Create a trip with 20 dummy points
viaggio_id_heavy = "test_viaggio_heavy_20"
punti = []
for i in range(25):
    # random spread around padua
    lat = 45.4 + (i * 0.005)
    lon = 11.8 + (i * 0.005)
    punti.append({"codice_univoco": f"c_{i}", "lat": lat, "lon": lon})

main.get_db().collection('viaggi').document(viaggio_id_heavy).set({
    "punti": punti,
    "ddt_ids": ["dummy_1", "dummy_2"], # not actually fetching PDFs for optimization test
    "status": "bozza"
})

print(f"\n[TEST] Ottimizzazione con {len(punti)} DDT")
t0 = time.time()
res = main.core_ottimizza_viaggio(viaggio_id_heavy)
t1 = time.time()
elapsed = t1 - t0

print(f"Risultato: {res['status']}")
print(f"Tempo di esecuzione API: {elapsed:.2f}s")
print(f"Messaggio: {res.get('message')}")

if elapsed < 10:
    print("PASS: Prestazioni sotto i 10 secondi confermate.")
else:
    print("WARNING: Tempi eccessivamente lunghi per OR-Tools su 25 nodi.")
