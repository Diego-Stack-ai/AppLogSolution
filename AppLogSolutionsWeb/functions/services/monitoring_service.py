import typing
from datetime import date
from firebase_functions import https_fn
from infrastructure.firebase_setup import get_db

def handle_stats_giornaliere(req: https_fn.CallableRequest) -> typing.Any:
    oggi = str(date.today())
    stats_doc = get_db().collection('stats_operative').document(oggi).get()
    if stats_doc.exists:
        data = stats_doc.to_dict()
        return {
            "status": "ok",
            "message": "Stats caricate",
            "errori": [],
            "data": {
                "ddt_elaborati_oggi": data.get('count_elabora_pdf', 0),
                "viaggi_creati_oggi": data.get('count_ottimizza_viaggio', 0),
                "errori_giornata": data.get('errori_totali', 0),
                "tempo_medio_sec": data.get('tempo_medio', 0)
            }
        }
    return {"status": "ok", "message": "Nessuna operazione oggi", "errori": [], "data": {"ddt_elaborati_oggi": 0, "viaggi_creati_oggi": 0, "errori_giornata": 0, "tempo_medio_sec": 0}}

def handle_check_giornaliero(req: https_fn.CallableRequest) -> typing.Any:
    if not req.auth:
        raise https_fn.HttpsError(
            code=https_fn.FunctionsErrorCode.UNAUTHENTICATED,
            message="Non autorizzato."
        )
    print("[INFO] Start check_giornaliero")
    db = get_db()
    
    try:
        tenants = [doc.id for doc in db.collection('clienti').list_documents()]
    except Exception as e:
        print(f"[check_giornaliero] Errore lookup tenant: {e}")
        tenants = ['DNR', 'GRAN CHEF', 'CATTEL', 'DAC']
    ddt_non_assegnati = 0
    clienti_senza_coordinate = 0
    viaggi_non_validi = 0

    for t in tenants:
        # 1. DDT nuovi non assegnati
        ddts = list(db.collection('clienti').document(t).collection('ddt').stream())
        ddt_non_assegnati += sum(1 for d in ddts if d.to_dict().get('stato') != 'assegnato')

        # 2. Clienti senza coordinate
        clienti = list(db.collection('clienti').document(t).collection('raccolta clienti').stream())
        for c in clienti:
            data = c.to_dict()
            lat, lon = data.get('lat'), data.get('lon')
            if not lat or not lon or lat == '0' or lat == '0.0':
                clienti_senza_coordinate += 1

        # 3. Viaggi incompleti (senza ddt o non completati)
        viaggi = list(db.collection('clienti').document(t).collection('viaggi ddt').stream())
        for v in viaggi:
            data = v.to_dict()
            ddt_ids = data.get('ddt_ids', [])
            stato = data.get('status', 'bozza')
            if not ddt_ids or stato == 'bozza':
                viaggi_non_validi += 1

    status_code = "ok" if (ddt_non_assegnati == 0 and clienti_senza_coordinate == 0 and viaggi_non_validi == 0) else "attenzione"
    
    return {
        "status": status_code,
        "message": "Check completato",
        "errori": [],
        "data": {
            "ddt_non_assegnati": ddt_non_assegnati,
            "clienti_senza_coordinate": clienti_senza_coordinate,
            "viaggi_non_validi": viaggi_non_validi
        }
    }
