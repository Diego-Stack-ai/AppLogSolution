import os
import io
import time
from flask import Flask, jsonify
import firebase_admin
from firebase_admin import firestore, storage
from pypdf import PdfReader, PdfWriter
import pdfplumber
import re

# Inizializzazione Firebase Admin
if not firebase_admin._apps:
    firebase_admin.initialize_app()

db = firestore.client()
bucket_name = os.environ.get("BUCKET_NAME", "log-solution-60007.firebasestorage.app")
bucket = storage.bucket(bucket_name)

app = Flask(__name__)

# Regex predefinite per lo split
DATA_DDT_RE = re.compile(r'del\s+(\d{2})/(\d{2})/(\d{4})', re.I)
LUOGO_RE = re.compile(r'(?:[Ll]uogo [Dd]i [Dd]estinazione|[Cc]odice [Dd]estinazione):\s*([pP]\d{4,5})')

def _estrai_data_luogo(text):
    data = None
    m = DATA_DDT_RE.search(text)
    if m:
        data = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    luogo_m = LUOGO_RE.search(text)
    luogo = luogo_m.group(1).lower() if luogo_m else None
    return data, luogo

def map_customer_from_firestore(codice):
    """ Esempio di mapping cliente diretto da Firestore """
    if not codice or codice == "p00000": return None
    
    col = db.collection('customers').document('DNR').collection('gestione_nuovi_clienti')
    docs = list(col.where('Codice Frutta', '==', codice).limit(1).stream())
    if docs: return docs[0].to_dict()
    
    docs = list(col.where('Codice Latte', '==', codice).limit(1).stream())
    if docs: return docs[0].to_dict()
    
    return None

def process_single_job(job_id, job_data):
    try:
        job_ref = db.collection('customers').document('DNR').collection('processing_jobs').document(job_id)
        
        # 1. Aggiornamento stato a processing
        job_ref.update({
            'status': 'processing',
            'updated_at': firestore.SERVER_TIMESTAMP
        })
        
        storage_path = job_data.get('storage_path')
        tipo = job_data.get('type') # 'FRUTTA' o 'LATTE'
        
        print(f"[WORKER] Inizio elaborazione Job {job_id} ({tipo}) - File: {storage_path}")
        
        blob = bucket.blob(storage_path)
        if not blob.exists():
            raise Exception("File PDF originale non trovato nello Storage")
            
        pdf_bytes = blob.download_as_bytes()
        reader = PdfReader(io.BytesIO(pdf_bytes))
        
        creati = 0
        errori = []
        visti = {}
        
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            # 2. Loop per split DDT
            for i in range(len(pdf.pages)):
                try:
                    text = pdf.pages[i].extract_text() or ""
                    d, l = _estrai_data_luogo(text)
                    if not d or not l: continue
                    
                    chiave = (d, l)
                    cnt = visti.get(chiave, 0) + 1
                    visti[chiave] = cnt
                    
                    fname = f"{l}_{d}_{cnt}.pdf" if cnt > 1 else f"{l}_{d}.pdf"
                    percorso_out = f"split_ddt/{d}/{tipo}/{fname}"
                    
                    # Estrazione e Split del singolo DDT
                    writer = PdfWriter()
                    writer.add_page(reader.pages[i])
                    out_io = io.BytesIO()
                    writer.write(out_io)
                    out_io.seek(0)
                    
                    out_blob = bucket.blob(percorso_out)
                    out_blob.upload_from_file(out_io, content_type="application/pdf")
                    creati += 1
                    
                    # 3. Mapping Clienti da Firestore (Gestione Nuovi Clienti)
                    cliente_data = map_customer_from_firestore(l)
                    nome_cliente = cliente_data.get('A chi va consegnato') if cliente_data else "Sconosciuto"
                    
                    # 4. Creazione delivery log in Firestore
                    db.collection('customers').document('DNR').collection('deliveries').add({
                        "job_id": job_id,
                        "codice_cliente": l,
                        "nome_cliente": nome_cliente,
                        "data": d,
                        "tipo": tipo,
                        "storage_path": percorso_out,
                        "stato": "processato"
                    })
                    
                except Exception as ex_page:
                    errori.append(f"Errore pag {i}: {str(ex_page)}")
                
        # 5. Output Strutturato e Aggiornamento Job a completed
        job_ref.update({
            'status': 'completed',
            'result': {
                'ddt_estratti': creati,
                'errori_interni': len(errori),
                'messaggio': f"Elaborazione terminata: generati {creati} DDT."
            },
            'updated_at': firestore.SERVER_TIMESTAMP
        })
        print(f"[WORKER] Job {job_id} completato con successo. Creati: {creati}")
        
    except Exception as e:
        print(f"[WORKER] Errore critico in Job {job_id}: {str(e)}")
        # Aggiornamento in caso di Errore
        db.collection('customers').document('DNR').collection('processing_jobs').document(job_id).update({
            'status': 'error',
            'error_message': str(e),
            'updated_at': firestore.SERVER_TIMESTAMP
        })

@app.route('/process', methods=['POST', 'GET'])
def process_pending_jobs():
    """
    Endpoint HTTP per eseguire il pulling della coda.
    Può essere triggerato via HTTP da Cloud Scheduler (ogni minuto)
    o via Eventarc.
    """
    jobs_ref = db.collection('customers').document('DNR').collection('processing_jobs')
    pending_jobs = jobs_ref.where('status', '==', 'uploaded').limit(5).stream()
    
    processed_count = 0
    for job in pending_jobs:
        process_single_job(job.id, job.to_dict())
        processed_count += 1
        
    return jsonify({
        "status": "success", 
        "message": f"Worker eseguito. Processati {processed_count} jobs."
    })

if __name__ == "__main__":
    # Avvio server Flask (Cloud Run imposterà la env var PORT)
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
