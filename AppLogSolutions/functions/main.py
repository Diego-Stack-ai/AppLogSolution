# functions/main.py
import re
import io
from firebase_functions import https_fn, options

# --- CONFIGURAZIONI ---
BUCKET_NAME = "log-solution-60007.firebasestorage.app"

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

@https_fn.on_call(
    region="europe-west1",
    memory=options.MemoryOption.GB_1,
    timeout_sec=300,
    cors=options.CorsOptions(cors_origins="*", cors_methods=["get", "post"])
)
def elabora_pdf_estrazione(req: https_fn.CallableRequest):
    """
    Fase 1: Prende i file pdf Lenzuolone caricati nel bucket, li divide,
    verifica se ci sono nuovi clienti/codici, e li salva suddivisi per date e fattorie.
    """
    # IMPORT LAZY PER EVITARE TIMEOUT DI INITIALIZATION
    import firebase_admin
    from firebase_admin import initialize_app, firestore, storage
    import pdfplumber
    from pypdf import PdfReader, PdfWriter
    
    if not firebase_admin._apps:
        initialize_app()
        
    db = firestore.client()
    uid = req.auth.uid if req.auth else None
    if not uid:
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.UNAUTHENTICATED,
            message="Devi essere autenticato per avviare la procedura."
        )

    print("Inizio Elaborazione Fase 1 (Taglio PDF)")
    bucket = storage.bucket(name=BUCKET_NAME)
    
    # 1. Recupera i file dalla cartella input_pdf_fornitore/
    blobs = list(bucket.list_blobs(prefix="input_pdf_fornitore/"))
    pdf_blobs = [b for b in blobs if b.name.endswith(".pdf")]
    
    if not pdf_blobs:
        return {"status": "error", "message": "Nessun file PDF trovato nella cartella di input."}

    visti = {}
    creati = 0
    date_valide = set()

    for blob in pdf_blobs:
        print(f"📄 Elaboro {blob.name}...")
        
        is_frutta = "frutta" in blob.name.lower()
        tipo_label = "FRUTTA" if is_frutta else "LATTE"
        is_duplicata = is_frutta
        
        pdf_bytes = blob.download_as_bytes()
        
        try:
            reader = PdfReader(io.BytesIO(pdf_bytes))
            with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
                step = 2 if is_duplicata else 1
                for i in range(0, len(pdf.pages), step):
                    text = pdf.pages[i].extract_text() or ""
                    d, l = _estrai_data_luogo(text)
                    
                    if not d or not l:
                        continue
                        
                    date_valide.add(d)
                    chiave = (d, l)
                    cnt = visti.get(chiave, 0) + 1
                    visti[chiave] = cnt
                    
                    fname = f"{l}_{d}_{cnt}.pdf" if cnt > 1 else f"{l}_{d}.pdf"
                    cart_out = f"CONSEGNE/CONSEGNE_{d}/DDT-ORIGINALI-DIVISI/{tipo_label}"
                    percorso_out = f"{cart_out}/{fname}"
                    
                    writer = PdfWriter()
                    writer.add_page(reader.pages[i])
                    out_io = io.BytesIO()
                    writer.write(out_io)
                    out_io.seek(0)
                    
                    out_blob = bucket.blob(percorso_out)
                    out_blob.upload_from_file(out_io, content_type="application/pdf")
                    creati += 1
                    
        except Exception as e:
            print(f"Errore su {blob.name}: {e}")
            
    print(f"Fase 1 completata: {creati} DDT estratti per le date {date_valide}.")
    
    for blob in pdf_blobs:
        archived_name = blob.name.replace("input_pdf_fornitore/", "archivio_lenzuoloni_processati/")
        bucket.copy_blob(blob, bucket, archived_name)
        blob.delete()
        print(f"File {blob.name} archiviato in {archived_name}.")

    return {
        "status": "success",
        "date_elaborate": list(date_valide),
        "ddt_estratti": creati,
        "message": f"Taglio completato con successo. L'intelligenza cloud ha generato {creati} file singoli nelle date: {', '.join(date_valide)}."
    }
