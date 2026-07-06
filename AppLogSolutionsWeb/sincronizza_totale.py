import os
import firebase_admin
from firebase_admin import credentials, firestore

# ==============================================================================
# SCRIPT DI SINCRONIZZAZIONE TOTALE (PRODUZIONE -> SVILUPPO)
# Attenzione: Questo script copia l'INTERO database (tutte le collezioni, 
# documenti, sottocollezioni, storico logistico, ecc.)
# ==============================================================================

def copia_collezione(source_collection_ref, target_collection_ref, prefisso=""):
    """
    Funzione ricorsiva che copia tutti i documenti di una collezione e 
    cerca automaticamente eventuali sottocollezioni all'interno di ogni documento.
    """
    documenti = source_collection_ref.stream()
    conteggio = 0

    for doc in documenti:
        doc_data = doc.to_dict() or {}
        # Copia il documento corrente
        target_collection_ref.document(doc.id).set(doc_data)
        conteggio += 1
        
        # Cerca sottocollezioni all'interno di questo documento
        sottocollezioni = doc.reference.collections()
        for sub_coll in sottocollezioni:
            print(f"{prefisso}  ↳ Trovata sottocollezione '{sub_coll.id}' in '{doc.id}', avvio copia...")
            copia_collezione(
                source_collection_ref=sub_coll,
                target_collection_ref=target_collection_ref.document(doc.id).collection(sub_coll.id),
                prefisso=prefisso + "    "
            )
            
    if conteggio > 0:
        print(f"{prefisso}✔ Copiati {conteggio} documenti in '{source_collection_ref.id}'")

def main():
    if not os.path.exists("prod_key.json") or not os.path.exists("dev_key.json"):
        print("ERRORE: Mancano i file delle chiavi (prod_key.json o dev_key.json).")
        return

    print("Inizializzazione connessioni...")
    # Inizializza Produzione
    cred_prod = credentials.Certificate("prod_key.json")
    app_prod = firebase_admin.initialize_app(cred_prod, name='prod_full')
    db_prod = firestore.client(app=app_prod)

    # Inizializza Sviluppo
    cred_dev = credentials.Certificate("dev_key.json")
    app_dev = firebase_admin.initialize_app(cred_dev, name='dev_full')
    db_dev = firestore.client(app=app_dev)

    print("=====================================================")
    print("INIZIO COPIA TOTALE: DA PRODUZIONE A SVILUPPO")
    print("Nota: Questa operazione potrebbe richiedere diversi minuti")
    print("a seconda della dimensione dello storico aziendale.")
    print("=====================================================\n")

    # Ottieni tutte le collezioni radice (root collections) del database di produzione
    collezioni_radice = db_prod.collections()
    
    for collezione in collezioni_radice:
        print(f"Analisi Collezione Radice: [{collezione.id}]")
        copia_collezione(
            source_collection_ref=collezione,
            target_collection_ref=db_dev.collection(collezione.id),
            prefisso=""
        )

    print("\n=====================================================")
    print("SINCRONIZZAZIONE TOTALE COMPLETATA CON SUCCESSO!")
    print("Ora l'app di sviluppo è una copia carbone di quella di produzione.")
    print("=====================================================")

if __name__ == "__main__":
    main()
