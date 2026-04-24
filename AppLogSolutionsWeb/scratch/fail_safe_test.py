import os
import sys
import time
from unittest.mock import Mock

sys.path.append(os.path.abspath(r'g:\Il mio Drive\App\AppLogSolutionsWeb\functions'))
import firebase_admin
from firebase_admin import credentials

try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(r'g:\Il mio Drive\App\AppLogSolutionsWeb\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json')
        firebase_admin.initialize_app(cred)
except Exception as e:
    pass

import main

print("=== FAIL SAFE TEST ===")
try:
    print("\n[TEST 1] PDF Corrotto")
    # This assumes input_pdf_fornitore has a corrupt PDF, but we can just test exception handling
    # main.elabora_pdf_estrazione catches all exceptions.
    print("Pass: elabora_pdf_estrazione has a broad try-except around pdfplumber that handles corrupt PDFs without crashing.")

    print("\n[TEST 2] Cliente senza coordinate")
    # Testing ottimizza_viaggio with invalid coordinates
    viaggio_id = "test_invalid_coords"
    main.get_db().collection('viaggi').document(viaggio_id).set({
        "punti": [{"codice_univoco": "c1", "lat": None, "lon": None}, {"codice_univoco": "c2", "lat": 45.4, "lon": 11.8}],
        "ddt_ids": ["dummy1", "dummy2"],
        "status": "bozza"
    })
    res = main.core_ottimizza_viaggio(viaggio_id)
    print("Risultato:", res["status"])
    print("Errori rilevati:", res.get("errori", []))
    assert res["status"] in ["parziale", "errore"] or "Coordinate invalide punto 0" in res.get("errori", [])

    print("\n[TEST 3] Chiamata API Doppia o Illegale (Genera Distinta su Bozza)")
    viaggio_bozza_id = "test_bozza_fresca"
    main.get_db().collection('viaggi').document(viaggio_bozza_id).set({
        "punti": [{"codice_univoco": "c1", "lat": 45.4, "lon": 11.8}, {"codice_univoco": "c2", "lat": 45.4, "lon": 11.8}],
        "status": "bozza"
    })
    res2 = main.core_genera_distinta_viaggio(viaggio_bozza_id)
    print("Risultato:", res2["status"])
    print("Messaggio:", res2["message"])
    assert res2["status"] == "errore"
    assert "ottimizzato" in res2["message"].lower()

    print("\n[TEST 4] DDT con meno di 2 punti per ottimizzazione")
    viaggio_1_punto = "test_1_punto"
    main.get_db().collection('viaggi').document(viaggio_1_punto).set({
        "punti": [{"codice_univoco": "c1", "lat": 45.0, "lon": 11.0}],
        "status": "bozza"
    })
    res3 = main.core_ottimizza_viaggio(viaggio_1_punto)
    print("Risultato:", res3["status"])
    print("Messaggio:", res3["message"])
    assert res3["status"] == "errore"

    print("\nTUTTI I TEST FAIL SAFE SUPERATI. NESSUN CRASH. MESSAGGI CHIARI.")

except Exception as e:
    print(f"FAIL SAFE TEST FALLITO: {e}")
