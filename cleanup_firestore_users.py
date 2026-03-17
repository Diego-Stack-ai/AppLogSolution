import firebase_admin
from firebase_admin import credentials, firestore

key_path = r'g:\Il mio Drive\AppLogSolution\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json'
if not firebase_admin._apps:
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def cleanup_users():
    print("🚀 Inizio Ristrutturazione Firestore Utenti")
    print("-" * 50)
    
    users_ref = db.collection('users')
    docs = list(users_ref.stream())
    
    # Mappa per trovare duplicati per email
    email_to_uid_doc = {}
    docs_to_delete = []
    
    # Passaggio 1: Identificazione UID reali e pulizia dati
    for doc in docs:
        d = doc.to_dict()
        doc_id = doc.id
        email = d.get('email', '').lower().strip()
        
        # Pulizia campi
        updates = {}
        
        # Standardizza ruolo
        if 'ruolo' in d:
            new_role = d['ruolo'].lower().strip()
            if d['ruolo'] != new_role:
                updates['ruolo'] = new_role
                
        # Rimuovi password
        if 'password' in d:
            updates['password'] = firestore.DELETE_FIELD
            
        # Assicura campi obbligatori
        if 'nome' not in d: updates['nome'] = doc_id.replace('_', ' ').title()
        if 'tipoTurno' not in d: updates['tipoTurno'] = 'giornata'
        if 'canElevate' not in d: 
            updates['canElevate'] = True if d.get('ruolo') == 'amministratore' else False
            
        # Applica aggiornamenti al documento corrente
        if updates:
            print(f"🔧 Aggiornamento campi per {doc_id}: {list(updates.keys())}")
            users_ref.document(doc_id).update(updates)
            
        # Logica deduplicazione
        # Se l'ID del documento NON è lungo come un UID Firebase (tipicamente > 20 char)
        # e abbiamo un altro documento con lo stesso email che è un UID reale, lo segnamo per eliminazione
        if len(doc_id) < 20: # Probabile slug (es. diego_boschetto)
            if email in email_to_uid_doc:
                print(f"♻️ Trovato duplicato slug: {doc_id} (l'email {email} ha già un account UID)")
                docs_to_delete.append(doc_id)
            else:
                # Vediamo se esiste un UID reale per questa email in altri doc
                found_uid = False
                for other in docs:
                    if len(other.id) >= 20 and other.to_dict().get('email', '').lower() == email:
                        print(f"♻️ Trovato duplicato slug: {doc_id} -> Mappato a UID: {other.id}")
                        docs_to_delete.append(doc_id)
                        found_uid = True
                        break
        else:
            email_to_uid_doc[email] = doc_id

    # Passaggio 2: Eliminazione duplicati slug
    for slug_id in set(docs_to_delete):
        print(f"🗑️ Eliminazione profilo obsoleto: {slug_id}")
        users_ref.document(slug_id).delete()
        
    print("-" * 50)
    print("✅ Ristrutturazione Firestore Completata")

if __name__ == "__main__":
    cleanup_users()
