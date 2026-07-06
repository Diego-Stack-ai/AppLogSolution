import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

# ==============================================================================
# ISTRUZIONI PER L'USO:
# 1. Vai sulla console Firebase del progetto PRINCIPALE (log-solution-60007).
# 2. Vai su Impostazioni Progetto (ingranaggio in alto a sinistra) -> Account di Servizio.
# 3. Clicca su "Genera nuova chiave privata", rinomina il file scaricato in "prod_key.json" e mettilo in questa cartella.
# 4. Fai la stessa identica cosa sul nuovo progetto SVILUPPO (log-solutions-sviluppo).
# 5. Rinomina la chiave scaricata in "dev_key.json" e mettila in questa cartella.
# 6. Apri il terminale in questa cartella e lancia: python sincronizza_sviluppo.py
# ==============================================================================

def main():
    if not os.path.exists("prod_key.json") or not os.path.exists("dev_key.json"):
        print("ERRORE: Mancano i file delle chiavi (prod_key.json o dev_key.json). Leggi le istruzioni nel codice!")
        return

    # Inizializza Produzione
    cred_prod = credentials.Certificate("prod_key.json")
    app_prod = firebase_admin.initialize_app(cred_prod, name='prod')
    db_prod = firestore.client(app=app_prod)

    # Inizializza Sviluppo
    cred_dev = credentials.Certificate("dev_key.json")
    app_dev = firebase_admin.initialize_app(cred_dev, name='dev')
    db_dev = firestore.client(app=app_dev)

    print("--- INIZIO SINCRONIZZAZIONE ANAGRAFICHE ---")
    
    # 1. Copia i tenant (es. DNR, CATTEL, GRAN CHEF) ma SOLO le collezioni di base (anagrafiche)
    clienti_docs = db_prod.collection('clienti').stream()
    for tenant in clienti_docs:
        print(f"Copiando Tenant: {tenant.id}")
        db_dev.collection('clienti').document(tenant.id).set(tenant.to_dict() or {})
        
        # Copia anagrafiche interne essenziali (nomi reali dal DB)
        collezioni_da_copiare = ['codici articoli', 'raccolta clienti', 'impostazioni', 'magazzini_sedi', 'destinazioni_navette']
        for coll_name in collezioni_da_copiare:
            docs = db_prod.collection('clienti').document(tenant.id).collection(coll_name).stream()
            count = 0
            for doc in docs:
                db_dev.collection('clienti').document(tenant.id).collection(coll_name).document(doc.id).set(doc.to_dict() or {})
                count += 1
            print(f"  - Copiati {count} documenti da {coll_name}")

    print("--- SINCRONIZZAZIONE COMPLETATA ---")
    print("Nota: Gli utenti (login) devono essere ricreati manualmente nella console Firebase Sviluppo (Authentication),")
    print("oppure usa la pagina di registrazione dell'App Sviluppo per creare il tuo utente admin di prova.")

if __name__ == "__main__":
    main()
