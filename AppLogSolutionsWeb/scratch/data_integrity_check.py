import os
import sys

sys.path.append(os.path.abspath(r'g:\Il mio Drive\App\AppLogSolutionsWeb\functions'))

import firebase_admin
from firebase_admin import credentials, firestore

try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(r'g:\Il mio Drive\App\AppLogSolutionsWeb\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json')
        firebase_admin.initialize_app(cred)
except Exception as e:
    print(f"Errore init: {e}")

db = firestore.client()

def check_integrity():
    print("=== DATA INTEGRITY CHECK ===")
    
    # 1. Validare Mappatura Clienti (lat/lon)
    clienti = list(db.collection('mappatura').stream())
    clienti_anomali = []
    for c in clienti:
        data = c.to_dict()
        lat = data.get('lat')
        lon = data.get('lon')
        if not isinstance(lat, float) or not isinstance(lon, float):
            clienti_anomali.append(c.id)
            
    print(f"Clienti totali: {len(clienti)}")
    print(f"Clienti senza coordinate float: {len(clienti_anomali)}")
    if clienti_anomali:
        print(f"Anomalie Clienti (ID): {clienti_anomali[:10]}...")

    # 2. Validare DDT
    ddts = list(db.collection('ddt').stream())
    ddt_anomali = []
    clienti_keys = {c.id for c in clienti}
    codici_legacy_keys = {c.to_dict().get('codice_legacy', '') for c in clienti}
    
    for ddt in ddts:
        data = ddt.to_dict()
        cod_cliente = data.get('codice_cliente', '')
        if not cod_cliente or cod_cliente not in codici_legacy_keys:
            ddt_anomali.append(ddt.id)
            
    print(f"\nDDT totali: {len(ddts)}")
    print(f"DDT senza mapping o senza codice: {len(ddt_anomali)}")
    if ddt_anomali:
        print(f"Anomalie DDT (ID): {ddt_anomali[:10]}...")

    # 3. Validare Viaggi
    viaggi = list(db.collection('viaggi').stream())
    viaggi_anomali = []
    ddt_keys = {d.id for d in ddts}
    
    for v in viaggi:
        data = v.to_dict()
        v_ddt_ids = data.get('ddt_ids', [])
        if not v_ddt_ids:
            viaggi_anomali.append(f"{v.id} (vuoto)")
            continue
            
        for d_id in v_ddt_ids:
            if d_id not in ddt_keys:
                viaggi_anomali.append(f"{v.id} (DDT inesistente: {d_id})")
                
    print(f"\nViaggi totali: {len(viaggi)}")
    print(f"Viaggi con anomalie: {len(viaggi_anomali)}")
    if viaggi_anomali:
        print(f"Anomalie Viaggi: {viaggi_anomali[:10]}...")

if __name__ == '__main__':
    check_integrity()
