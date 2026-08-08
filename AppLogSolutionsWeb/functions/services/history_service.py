from firebase_admin import firestore
from firebase_functions import https_fn
from infrastructure.firebase_setup import get_db
import typing

def handle_rilascia_recupero_storico(req: https_fn.CallableRequest) -> typing.Any:
    """
    Elimina i record temporanei creati per l'R&D in viaggi ddt e reports_logistici.
    """
    data_consegna = req.data.get("data_consegna")
    if not data_consegna:
        return {"status": "errore", "message": "data_consegna mancante"}
        
    print(f"[R&D RILASCIO] Pulizia record sandbox per {data_consegna}...")
    db = get_db()
    
    try:
        # Elimina da reports_logistici se is_recupero_rd == True
        rep_ref = db.collection('clienti').document('report_logistici').collection('giornate').document(data_consegna)
        doc = rep_ref.get()
        if doc.exists and doc.to_dict().get("is_recupero_rd", False):
            rep_ref.delete()
            
        # Elimina da viaggi ddt in tutti i tenant
        try:
            tenants = [doc.id for doc in db.collection('clienti').list_documents() if doc.id != "report_logistici"]
        except:
            tenants = ["DNR", "CATTEL", "GRAN CHEF", "BAUER", "DAC"]
            
        count = 0
        for t in tenants:
            viaggi_ref = db.collection('clienti').document(t).collection('viaggi ddt')
            viaggi = viaggi_ref.where("data_lavoro", "==", data_consegna).where("is_recupero_rd", "==", True).stream()
            for v in viaggi:
                viaggi_ref.document(v.id).delete()
                count += 1
            
        print(f"[R&D RILASCIO] ✓ Pulizia completata per {data_consegna}. {count} record eliminati.")
        return {"status": "ok", "message": f"Sessione di studio per il {data_consegna} conclusa e ripulita con successo."}
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"status": "errore", "message": f"Errore rilascio sandbox: {str(e)}"}

