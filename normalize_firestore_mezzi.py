import firebase_admin
from firebase_admin import credentials, firestore

key_path = r'g:\Il mio Drive\AppLogSolution\backend\config\log-solution-60007-firebase-adminsdk-fbsvc-2cf3d0c171.json'
if not firebase_admin._apps:
    cred = credentials.Certificate(key_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

def normalize_mezzi():
    print("🚀 Avvio Normalizzazione Mezzi Firestore...")
    print("-" * 50)
    
    mezzi_ref = db.collection('mezzi')
    docs = list(mezzi_ref.stream())
    
    # Mappa: target_targa -> list of (doc_id, data)
    targa_groups = {}
    
    for doc in docs:
        d = doc.to_dict()
        doc_id = doc.id
        
        targa = d.get('targa', '').strip().upper()
        
        if not targa:
            print(f"⚠️ Documento {doc_id} non ha una 'targa' (o è vuota). Salto.")
            continue
            
        if targa not in targa_groups:
            targa_groups[targa] = []
        targa_groups[targa].append((doc_id, d))

    print(f"📊 Trovati {len(docs)} documenti totali, raggruppati in {len(targa_groups)} Targhe uniche.")

    for target_targa, docs_list in targa_groups.items():
        print(f"\n🔄 Analisi Targa: {target_targa}")
        
        # Cerchiamo se esiste già un doc_id uguale alla targa
        correct_doc = next((d for d in docs_list if d[0] == target_targa), None)
        
        if correct_doc:
            print(f"  ✓ Documento corretto trovato (ID = {target_targa}).")
            # Manteniamo questo ed eliminiamo eventuali duplicati con ID generato a caso
            for doc_id, data in docs_list:
                if doc_id != target_targa:
                    print(f"  🗑️ Trovato duplicato! Elimino: {doc_id}")
                    db.collection('mezzi').document(doc_id).delete()
        else:
            # Nessun documento ha ID == targa
            # Usiamo i dati dal primo
            source_id, source_data = docs_list[0]
            print(f"  ⚠️ Nessun doc con ID corretto. Creo nuovo {target_targa} copiando da {source_id}")
            
            new_data = source_data.copy()
            new_data['targa'] = target_targa # assicuriamo la targa in uppercase
            if 'modello' not in new_data:
                new_data['modello'] = ""
                
            db.collection('mezzi').document(target_targa).set(new_data)
            
            # Cancelliamo tutti i vecchi originali errati
            for doc_id, data in docs_list:
                print(f"  🗑️ Elimino originale con ID errato: {doc_id}")
                db.collection('mezzi').document(doc_id).delete()

    print("\n" + "="*50)
    print("✅ Normalizzazione Mezzi completata.")
    final_docs = list(db.collection('mezzi').stream())
    print(f"Totale documenti finali in 'mezzi': {len(final_docs)}")
    for doc in final_docs:
        d = doc.to_dict()
        print(f"  - ID: {doc.id} | Targa: {d.get('targa')} | Modello: {d.get('modello')}")

if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    normalize_mezzi()
