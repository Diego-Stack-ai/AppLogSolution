import os
import sys

sys.path.append(os.path.abspath(r'g:\Il mio Drive\App\AppLogSolutionsWeb\functions'))

import firebase_admin
from firebase_admin import credentials, firestore

def init_firebase():
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(r'g:\Il mio Drive\App\AppLogSolutionsWeb\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json')
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        print(f"Errore init: {e}")
        return None

def esegui_check_giornaliero():
    db = init_firebase()
    if not db:
        return {"error": "Firebase DB non inizializzato."}

    # 1. DDT nuovi non assegnati
    # Query: stato != 'assegnato'
    ddts = list(db.collection('ddt').stream())
    ddt_non_assegnati = sum(1 for d in ddts if d.to_dict().get('stato') != 'assegnato')

    # 2. Clienti senza coordinate valide
    # Query: lat == null o lon == null (o non validi)
    clienti = list(db.collection('mappatura').stream())
    clienti_senza_coordinate = 0
    for c in clienti:
        data = c.to_dict()
        lat, lon = data.get('lat'), data.get('lon')
        if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
            clienti_senza_coordinate += 1

    # 3. Viaggi incompleti
    # Query: senza ddt_ids oppure senza ordine_visita
    viaggi = list(db.collection('viaggi').stream())
    viaggi_non_validi = 0
    for v in viaggi:
        data = v.to_dict()
        ddt_ids = data.get('ddt_ids', [])
        ordine = data.get('ordine_visita', [])
        # Consideriamo non valido se mancano ddt o se non è ancora stato ottimizzato
        if not ddt_ids or not ordine:
            viaggi_non_validi += 1

    output = {
        "ddt_non_assegnati": ddt_non_assegnati,
        "clienti_senza_coordinate": clienti_senza_coordinate,
        "viaggi_non_validi": viaggi_non_validi
    }

    print("=== CHECK GIORNALIERO AUTOMATICO ===")
    print(f"DDT non assegnati: {output['ddt_non_assegnati']}")
    print(f"Clienti da mappare (lat/lon mancanti): {output['clienti_senza_coordinate']}")
    print(f"Viaggi incompleti (da ottimizzare o vuoti): {output['viaggi_non_validi']}")
    
    return output

if __name__ == '__main__':
    esegui_check_giornaliero()
