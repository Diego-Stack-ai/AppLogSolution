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
