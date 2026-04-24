import os
import sys
from unittest.mock import Mock

# Aggiungi cartella functions al path
sys.path.append(os.path.abspath(r'g:\Il mio Drive\App\AppLogSolutionsWeb\functions'))

import firebase_admin
from firebase_admin import credentials, firestore, storage

# Inizializza firebase admin se necessario
try:
    if not firebase_admin._apps:
        cred = credentials.Certificate(r'g:\Il mio Drive\App\AppLogSolutionsWeb\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json')
        firebase_admin.initialize_app(cred)
except Exception as e:
    print(f"Errore init: {e}")

db = firestore.client()
bucket = storage.bucket('log-solution-60007.firebasestorage.app')

def setup_config():
    print("--- TASK 4: SETUP CONFIG ---")
    articoli_noti = [
        "10-FLYER", "10-GEL", "10-MANIFESTO", "10-AT-01", "10-BICC", "10-CUCCH", "10-PIATTO",
        "AP-SU-PC", "FO-DI-PV-04-LB", "FO-DI-GP-01-NI", "FVNS-03", "FVNS-03-", 
        "LT-AQ-04-LV", "LT-AQ-04-LB", "LT-AQ-04-LS", "LT-DL-02-LC", "LT-ES-04-LS", "LT-ESL-IN-LB", 
        "MA-T-LI-L3-NA", "ME-T-DI-V0-NA", "ME-S-BI-L3-NA", "PE-T-DI-L3-NA",
        "YO-BI-MN-04-LB", "YO-DL-02-LC", "FI-Z-BI-L3-NA", "FR-M-BI-L3-NI",
        "LNS-04-GADGET", "LNS-04-", "CA-Z-BI-L3-NA", "KI-S-BI-L3-NA"
    ]
    db.collection('config').document('app').set({'ARTICOLI_NOTI': articoli_noti})
    print("Config salvata in config/app.")

def setup_dummy_pdf():
    print("--- TASK 1: CREAZIONE DUMMY PDF ---")
    try:
        from reportlab.pdfgen import canvas
        c = canvas.Canvas("dummy.pdf")
        c.drawString(100, 750, "Documento di Trasporto del 15/04/2026")
        c.drawString(100, 730, "Luogo Di Destinazione: p9999")
        c.drawString(100, 710, "Cod. Articolo          Descrizione                  Q.ta")
        c.drawString(100, 690, "10-FLYER               Volantino Pubblicitario      100 Pz")
        c.save()
        
        blob = bucket.blob("input_pdf_fornitore/dummy_frutta.pdf")
        blob.upload_from_filename("dummy.pdf")
        print("Dummy PDF caricato in Storage.")
    except Exception as e:
        print(f"Errore creazione dummy PDF: {e}")

def run_tests():
    # Importa main dopo aver inizializzato l'app
    import main
    
    print("\n--- ESECUZIONE ELABORA PDF ---")
    res1 = main.core_elabora_pdf_estrazione("test_user_id")
    print("Risultato estrazione:", res1)
    
    if res1.get('status') == 'errore' and not res1.get('data', {}).get('ddt_estratti', 0):
        print("Test fallito: nessun DDT estratto.")
        return

    # Trova il ddt creato
    ddt_docs = list(db.collection('ddt').where('codice_cliente', '==', 'p9999').stream())
    if not ddt_docs:
        print("Nessun DDT trovato nel db!")
        return
    
    ddt_id = ddt_docs[0].id
    print(f"DDT trovato: {ddt_id}")
    
    print("\n--- CREAZIONE VIAGGIO DUMMY ---")
    viaggio_data = {
        "data": "15-04-2026",
        "nome_giro": "Giro Test",
        "ddt_ids": [ddt_id],
        "punti": [
            {"codice_univoco": "p9999_x", "lat": 45.40, "lon": 11.87},
            {"codice_univoco": "p8888_x", "lat": 45.42, "lon": 11.89}
        ]
    }
    viaggio_ref = db.collection('viaggi').document('viaggio_test_123')
    viaggio_ref.set(viaggio_data)
    print("Viaggio creato.")

    print("\n--- ESECUZIONE GENERA DISTINTA ---")
    res2 = main.core_genera_distinta_viaggio("viaggio_test_123")
    print("Risultato distinta:", res2)

    print("\n--- ESECUZIONE OTTIMIZZA VIAGGIO ---")
    res3 = main.core_ottimizza_viaggio("viaggio_test_123")
    print("Risultato ottimizzazione:", res3)
    
    # Cleanup
    try:
        viaggio_ref.delete()
        db.collection('ddt').document(ddt_id).delete()
        if 'pdf_url' in res2.get('data', {}):
            pdf_path = res2['data']['pdf_url'].replace(f"gs://{main.BUCKET_NAME}/", "")
            bucket.blob(pdf_path).delete()
    except Exception as e:
        pass

if __name__ == '__main__':
    setup_config()
    setup_dummy_pdf()
    run_tests()
