import os
import io
import time
from flask import Flask, request, jsonify
from legacy_parser_adapter import processa_pdf_in_memoria

# Inizializzazione Firebase Admin (in produzione prende le credenziali automatiche)
import firebase_admin
from firebase_admin import credentials, firestore, storage

if not firebase_admin._apps:
    firebase_admin.initialize_app()

db = firestore.client()
bucket = storage.bucket(os.getenv("BUCKET_NAME", "log-solution-60007.firebasestorage.app"))

app = Flask(__name__)

def run_cloud_pipeline(job_id: str):
    """
    Esegue la pipeline cloud su un job specifico.
    """
    job_ref = db.collection('customers').document('DNR').collection('processing_jobs').document(job_id)
    job_doc = job_ref.get()
    
    if not job_doc.exists:
        return {"error": "Job non trovato"}
        
    data = job_doc.to_dict()
    if data.get("status") != "uploaded":
        return {"error": "Job già processato o in errore"}
        
    # Lock del job
    job_ref.update({"status": "processing"})
    
    storage_path = data.get("storage_path")
    etichetta = data.get("type", "FRUTTA")
    
    try:
        # 1. Recupero Mappatura Clienti (Mock db_mappati)
        # Qui potremmo leggere da db.collection('customers').document('DNR').collection('gestione_nuovi_clienti')
        # Per ora passiamo vuoto per forzare l'estrazione dati nuovi per testing, oppure leggiamo.
        clienti_ref = db.collection('customers').document('DNR').collection('gestione_nuovi_clienti')
        db_mappati = {doc.id: doc.to_dict() for doc in clienti_ref.stream()}
        
        # 2. Download PDF da Storage in memoria
        start_time = time.time()
        blob = bucket.blob(storage_path)
        pdf_bytes = blob.download_as_bytes()
        
        # 3. Chiamata al Legacy Wrapper
        risultato = processa_pdf_in_memoria(pdf_bytes, etichetta, db_mappati)
        
        # 4. Upload dei file split su Storage e salvataggio Deliveries
        split_files = risultato["split_files"]
        deliveries = risultato["deliveries"]
        nuovi_dati = risultato["nuovi_dati"]
        
        data_elaborazione = deliveries[0]["data"] if deliveries else "01-01-2099"
        
        for fname, out_stream in split_files.items():
            split_blob = bucket.blob(f"split_ddt/{data_elaborazione}/{etichetta}/{fname}")
            split_blob.upload_from_file(out_stream, content_type='application/pdf')
            
        # 5. Salvataggio nuovi clienti in Firestore
        for l, info in nuovi_dati.items():
            db.collection('customers').document('DNR').collection('gestione_nuovi_clienti').document(l).set(info, merge=True)
            
        # 6. Aggiornamento job e inserimento deliveries
        batch = db.batch()
        for deliv in deliveries:
            deliv_ref = db.collection('customers').document('DNR').collection('deliveries').document()
            batch.set(deliv_ref, deliv)
        batch.commit()
        
        elapsed = time.time() - start_time
        
        job_ref.update({
            "status": "completed",
            "pdf_generati": len(split_files),
            "nuovi_clienti": len(nuovi_dati),
            "tempo_sec": round(elapsed, 2)
        })
        
        return {
            "status": "success",
            "pdf_generati": len(split_files),
            "tempo_sec": round(elapsed, 2)
        }
        
    except Exception as e:
        job_ref.update({"status": "error", "error_message": str(e)})
        return {"error": str(e)}

@app.route('/process', methods=['POST'])
def process_endpoint():
    req = request.get_json()
    job_id = req.get("job_id")
    if not job_id:
        return jsonify({"error": "Missing job_id"}), 400
    res = run_cloud_pipeline(job_id)
    return jsonify(res)

if __name__ == '__main__':
    # Esecuzione locale
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8080)))
