import firebase_admin
from firebase_admin import credentials, firestore

# Configurazione
key_path = r'g:\Il mio Drive\AppLogSolution\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json'
if not firebase_admin._apps:
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def main():
    print("Avvio sistema di normalizzazione utenti Firestore...")
    users_ref = db.collection('users')
    docs = list(users_ref.stream())
    
    # 1. Raccogliamo e raggruppiamo i documenti in base all'UID interno
    # Mappa: internal_uid -> list of docs
    uid_groups = {}
    
    for doc in docs:
        d = doc.to_dict()
        doc_id = doc.id
        internal_uid = d.get('uid')
        
        if not internal_uid:
            print(f"Documento {doc_id} non ha un campo 'uid'. Lo ignoro.")
            continue
            
        if internal_uid not in uid_groups:
            uid_groups[internal_uid] = []
        uid_groups[internal_uid].append((doc_id, d))

    print(f"Trovati {len(docs)} documenti totali, raggruppati in {len(uid_groups)} UID unici.")

    for target_uid, docs_list in uid_groups.items():
        print(f"\nAnalisi UID: {target_uid}")
        
        # Cerco se esiste gia' un documento con ID uguale al target_uid
        target_doc = next((d for d in docs_list if d[0] == target_uid), None)
        
        if target_doc:
            print(f"  - Documento corretto trovato (ID = UID: {target_uid}).")
            target_data = target_doc[1]
            
            # 3. Eliminiamo eventuali duplicati per questo stesso UID che hanno ID doc sbagliato
            for doc_id, data in docs_list:
                if doc_id != target_uid:
                    print(f"  - Trovato duplicato! Elimino: {doc_id}")
                    db.collection('users').document(doc_id).delete()
            
            # 4. Verificare che ogni documento finale abbia i campi richiesti
            updates = {}
            if 'nome' not in target_data or not target_data['nome']: updates['nome'] = "Sconosciuto"
            if 'email' not in target_data or not target_data['email']: updates['email'] = "nessuna@email.com"
            if 'ruolo' not in target_data or not target_data['ruolo']: updates['ruolo'] = "autista"
            
            if updates:
                print(f"  - Aggiungo campi mancanti al doc {target_uid}: {updates}")
                db.collection('users').document(target_uid).update(updates)
                
        else:
            # 2. Se ID documento != uid interno per tutti, e non esiste il doc target
            # Prendiamo i dati dal primo documento della lista per creare quello corretto
            source_id, source_data = docs_list[0]
            print(f"  - Nessun documento ha ID = UID. Creo nuovo documento {target_uid} copiando da {source_id}")
            
            new_data = source_data.copy()
            # 4. Verifica campi richiesti:
            if 'nome' not in new_data or not new_data['nome']: new_data['nome'] = "Sconosciuto"
            if 'email' not in new_data or not new_data['email']: new_data['email'] = "nessuna@email.com"
            if 'ruolo' not in new_data or not new_data['ruolo']: new_data['ruolo'] = "autista"
            
            # Copiare tutti i dati -> creare nuovo documento
            db.collection('users').document(target_uid).set(new_data)
            
            # Eliminare tutti i documenti originali (che hanno ID errato)
            for doc_id, data in docs_list:
                print(f"  - Elimino documento originale con ID errato: {doc_id}")
                db.collection('users').document(doc_id).delete()

    # Verifica finale
    print("\n" + "="*50)
    print("Normalizzazione completata.")
    final_docs = list(db.collection('users').stream())
    print(f"Totale documenti finali in 'users': {len(final_docs)}")
    for doc in final_docs:
        d = doc.to_dict()
        print(f"  - ID: {doc.id} | UID: {d.get('uid')} | Nome: {d.get('nome')} | Email: {d.get('email')} | Ruolo: {d.get('ruolo')}")


if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    main()
